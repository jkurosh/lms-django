from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.utils import timezone
from datetime import timedelta
import pandas as pd
from .models import Case, LabTest, Slide, UserProgress, UserObservation, UserProfile, CaseCategory, SubCategory

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(
        label='فایل اکسل را انتخاب کنید',
        help_text='فایل باید شامل ستون‌های: title, category, history, correct_diagnosis, explanation باشد'
    )


class SlideInline(admin.TabularInline):
    model = Slide
    extra = 1
    fields = ('thumbnail', 'image', 'description',)
    readonly_fields = ('thumbnail',)

    # نمایش پیش‌نمایش تصویر در اینلاین
    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px; border-radius:4px;" />', obj.image.url)
        return "-"
    thumbnail.short_description = "پیش‌نمایش"

class LabTestInline(admin.TabularInline):
    model = LabTest
    extra = 0  # چون تست‌های پیش‌فرض خودکار اضافه می‌شوند
    fields = ('lab_type', 'lab_name', 'normal_range', 'lab_result', 'order_index')
    classes = ('collapse',)
    readonly_fields = ('lab_type', 'lab_name', 'normal_range')  # فیلدهای پیش‌فرض فقط خواندنی

# TestInline removed - Test model not in use

# TestInline حذف شد

# get_form method حذف شد

@admin.action(description="اضافه کردن تست‌های پیش‌فرض به کیس‌های انتخاب‌شده")
def add_default_lab_tests(modeladmin, request, queryset):
    """اضافه کردن تست‌های پیش‌فرض به کیس‌های انتخاب‌شده"""
    from .models import LabTest
    
    for case in queryset:
        # بررسی اینکه آیا تست‌های پیش‌فرض قبلاً وجود دارند
        if not case.lab_tests.filter(lab_type='CBC').exists():
            LabTest.objects.create(
                case=case,
                lab_type='CBC',
                lab_name='Complete Blood Count',
                normal_range='Normal ranges vary by species',
                lab_result='',
                order_index=1
            )
        
        if not case.lab_tests.filter(lab_type='CHEM').exists():
            LabTest.objects.create(
                case=case,
                lab_type='CHEM',
                lab_name='Clinical Chemistry Panel',
                normal_range='Normal ranges vary by species',
                lab_result='',
                order_index=2
            )
        
        if not case.lab_tests.filter(lab_type='MORPHO').exists():
            LabTest.objects.create(
                case=case,
                lab_type='MORPHO',
                lab_name='Morphological Changes',
                normal_range='No abnormalities expected',
                lab_result='',
                order_index=3
            )
    
    modeladmin.message_user(request, f'تست‌های پیش‌فرض به {queryset.count()} کیس اضافه شد.')

@admin.action(description="ساخت کپی از کیس‌های انتخاب‌شده")
def duplicate_cases(modeladmin, request, queryset):
    for obj in queryset:
        labtests = list(obj.lab_tests.all())
        slides = list(obj.slides.all())
        # tests = list(obj.tests.all())  # Test model not in use
        obj.pk = None  # کپی شیء اصلی
        obj.title = f"{obj.title} (کپی)"
        obj.save()
        # کپی روابط فرزند
        for lt in labtests:
            lt.pk = None
            lt.case = obj
            lt.save()
        for sl in slides:
            sl.pk = None
            sl.case = obj
            sl.image.save(sl.image.name, sl.image.file, save=True)  # حفظ فایل
            sl.save()
        # for tst in tests:  # Test model not in use
        #     tst.pk = None
        #     tst.case = obj
        #     tst.save()

@admin.action(description="اضافه کردن تست‌ها و مشاهدات به کیس‌های انتخاب‌شده")
def add_tests_to_cases(modeladmin, request, queryset):
    lab_tests_created = 0
    for case in queryset:
        try:
            # بررسی اینکه آیا تست‌ها قبلاً وجود دارند
            if case.lab_tests.count() == 0:
                # ایجاد تست‌های نمونه
                sample_tests = [
                    {
                        'test_type': 'CBC',
                        'name': 'Hemoglobin',
                        'reference_range': '12-18 g/dL',
                        'value': '15 g/dL',
                        'report': 'مقدار طبیعی'
                    },
                    {
                        'test_type': 'CBC',
                        'name': 'WBC',
                        'reference_range': '4.5-11.0 K/μL',
                        'value': '8.5 K/μL',
                        'report': 'مقدار طبیعی'
                    },
                    {
                        'test_type': 'CHEM',
                        'name': 'Glucose',
                        'reference_range': '70-110 mg/dL',
                        'value': '95 mg/dL',
                        'report': 'مقدار طبیعی'
                    },
                    {
                        'test_type': 'OTHER',
                        'name': 'Urinalysis',
                        'reference_range': 'Negative',
                        'value': 'Positive',
                        'report': 'وجود پروتئین در ادرار'
                    }
                ]
                for test_data in sample_tests:
                    try:
                        LabTest.objects.create(
                            case=case,
                            **test_data
                        )
                        lab_tests_created += 1
                    except Exception as e:
                        messages.warning(request, f'خطا در ایجاد تست {test_data["name"]}: {str(e)}')
                messages.info(request, f'{lab_tests_created} تست آزمایشگاهی ایجاد شد.')

            # مشاهدات از طریق UserObservation مدیریت می‌شوند
            messages.info(request, f'تست‌های آزمایشگاهی برای کیس {case.title} ایجاد شد.')

        except Exception as e:
            messages.error(request, f'خطا در پردازش کیس {case.title}: {str(e)}')

class CaseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'cases_count')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def cases_count(self, obj):
        return obj.cases.count()
    cases_count.short_description = 'تعداد کیس‌ها'

class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'labs_count', 'tests_count', 'slides_count', 'cbc_options', 'chem_options', 'morpho_options', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'history')
    actions = [duplicate_cases, add_tests_to_cases, add_default_lab_tests]
    inlines = [LabTestInline, SlideInline]

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'category', 'history', 'correct_diagnosis', 'explanation')
        }),
        ('اطلاعات اضافی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.import_excel_view, name='cases_case_import_excel'),
        ]
        return custom_urls + urls

    def import_excel_view(self, request):
        if request.method == 'POST':
            form = ExcelImportForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    excel_file = form.cleaned_data['excel_file']
                    df = pd.read_excel(excel_file)
                    
                    created_count = 0
                    for _, row in df.iterrows():
                        Case.objects.create(
                            title=row.get('title', ''),
                            category=CaseCategory.objects.first(),  # استفاده از اولین دسته‌بندی موجود
                            history=row.get('history', ''),
                            correct_diagnosis=row.get('correct_diagnosis', ''),
                            explanation=row.get('explanation', '')
                        )
                        created_count += 1
                    
                    messages.success(request, f'{created_count} کیس با موفقیت از فایل اکسل ایجاد شد.')
                    return HttpResponseRedirect(reverse('admin:cases_case_changelist'))
                except Exception as e:
                    messages.error(request, f'خطا در پردازش فایل اکسل: {str(e)}')
        else:
            form = ExcelImportForm()
        
        context = {
            'form': form,
            'title': 'وارد کردن کیس‌ها از فایل اکسل',
        }
        return render(request, 'admin/cases/case/import_excel.html', context)


    def labs_count(self, obj):
        return obj.lab_tests.count()
    labs_count.short_description = 'تعداد تست‌های آزمایشگاهی'

    def tests_count(self, obj):
        return obj.lab_tests.count()
    tests_count.short_description = 'تعداد تست‌های آزمایشگاهی'
    
    def cbc_options(self, obj):
        """نمایش گزینه‌های پیش‌فرض CBC"""
        from .models import CBC_DEFAULT_OPTIONS
        return ', '.join(CBC_DEFAULT_OPTIONS[:5]) + '...' if len(CBC_DEFAULT_OPTIONS) > 5 else ', '.join(CBC_DEFAULT_OPTIONS)
    cbc_options.short_description = 'گزینه‌های CBC'
    
    def chem_options(self, obj):
        """نمایش گزینه‌های پیش‌فرض CHEM"""
        from .models import CHEM_DEFAULT_OPTIONS
        return ', '.join(CHEM_DEFAULT_OPTIONS[:5]) + '...' if len(CHEM_DEFAULT_OPTIONS) > 5 else ', '.join(CHEM_DEFAULT_OPTIONS)
    chem_options.short_description = 'گزینه‌های CHEM'
    
    def morpho_options(self, obj):
        """نمایش گزینه‌های پیش‌فرض MORPHO"""
        from .models import MORPHO_DEFAULT_OPTIONS
        return ', '.join(MORPHO_DEFAULT_OPTIONS[:5]) + '...' if len(MORPHO_DEFAULT_OPTIONS) > 5 else ', '.join(MORPHO_DEFAULT_OPTIONS)
    morpho_options.short_description = 'گزینه‌های MORPHO'

    def slides_count(self, obj):
        return obj.slides.count()
    slides_count.short_description = 'تعداد اسلایدها'

class LabTestAdmin(admin.ModelAdmin):
    list_display = ('lab_name', 'case', 'lab_type', 'lab_result', 'normal_range')
    list_filter = ('lab_type', 'case__category')
    search_fields = ('lab_name', 'case__title')
    fields = ('case', 'lab_type', 'lab_name', 'normal_range', 'lab_result', 'order_index')

class SlideAdmin(admin.ModelAdmin):
    list_display = ('case', 'thumbnail_preview', 'description_short')
    list_filter = ('case__category',)
    search_fields = ('description', 'case__title')
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        if obj.image:
            # obj.image یک CharField است که نام فایل را ذخیره می‌کند
            image_url = f"/media/slides/{obj.image}"
            return format_html('<img src="{}" style="height:60px; border-radius:4px;" />', image_url)
        return "-"
    thumbnail_preview.short_description = "پیش‌نمایش"

    def description_short(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
    description_short.short_description = "توضیحات"

# TestOptionInline حذف شد

# TestAdmin حذف شد

class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'case', 'completed', 'score', 'attempts', 'completed_at')
    list_filter = ('completed', 'case__category', 'completed_at')
    search_fields = ('user__username', 'case__title')
    readonly_fields = ('accuracy_percentage',)

    def accuracy_percentage(self, obj):
        return f"{obj.accuracy_percentage}%"
    accuracy_percentage.short_description = 'درصد دقت'


# TestAdmin removed - Test model not in use

class UserObservationAdmin(admin.ModelAdmin):
    list_display = ('case', 'case_test', 'observation_text', 'is_correct', 'is_correct_display', 'created_at')
    list_filter = ('case', 'is_correct', 'case_test__lab_type', 'created_at')
    search_fields = ('observation_text', 'case__title', 'case_test__lab_type')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_correct',)
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('case', 'case_test', 'observation_text', 'is_correct', 'explanation')
        }),
        ('تنظیمات', {
            'fields': ('order_index',)
        }),
        ('سیستمی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_correct_display(self, obj):
        if obj.is_correct:
            return format_html('<span style="color: green; font-weight: bold;">✓ صحیح</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">✗ غلط</span>')
    is_correct_display.short_description = 'وضعیت'
    is_correct_display.admin_order_field = 'is_correct'
    
    actions = ['mark_as_correct', 'mark_as_incorrect', 'toggle_correct_status']
    
    @admin.action(description="علامت‌گذاری به عنوان صحیح")
    def mark_as_correct(self, request, queryset):
        updated = queryset.update(is_correct=True)
        self.message_user(request, f'{updated} مشاهده به عنوان صحیح علامت‌گذاری شد.')
    
    @admin.action(description="علامت‌گذاری به عنوان غلط")
    def mark_as_incorrect(self, request, queryset):
        updated = queryset.update(is_correct=False)
        self.message_user(request, f'{updated} مشاهده به عنوان غلط علامت‌گذاری شد.')
    
    @admin.action(description="تغییر وضعیت صحیح/غلط")
    def toggle_correct_status(self, request, queryset):
        for obj in queryset:
            obj.is_correct = not obj.is_correct
            obj.save()
        self.message_user(request, f'وضعیت {queryset.count()} مشاهده تغییر کرد.')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_cases_completed', 'overall_accuracy', 'diagnosis_accuracy', 'last_activity')
    list_filter = ('created_at', 'last_activity')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('overall_accuracy', 'diagnosis_accuracy', 'last_activity', 'created_at')
    actions = ['activate_30_days', 'extend_30_days', 'clear_subscription']

    @admin.action(description="فعال‌سازی اشتراک 30 روزه")
    def activate_30_days(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        end_date = now + timedelta(days=30)
        
        for profile in queryset:
            profile.set_subscription(now, end_date)
        
        self.message_user(request, f'{queryset.count()} اشتراک 30 روزه فعال شد.')

    @admin.action(description="تمدید 30 روزه اشتراک")
    def extend_30_days(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        
        for profile in queryset:
            if profile.subscription_end:
                new_end = profile.subscription_end + timedelta(days=30)
                profile.set_subscription(profile.subscription_start, new_end)
            else:
                now = timezone.now()
                end_date = now + timedelta(days=30)
                profile.set_subscription(now, end_date)
        
        self.message_user(request, f'{queryset.count()} اشتراک 30 روز تمدید شد.')

    @admin.action(description="پاک کردن اشتراک")
    def clear_subscription(self, request, queryset):
        for profile in queryset:
            profile.set_subscription(None, None)
        
        self.message_user(request, f'{queryset.count()} اشتراک پاک شد.')

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    search_fields = ('name', 'description')

# ثبت مدل‌ها در پنل ادمین
admin.site.register(CaseCategory, CaseCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(LabTest, LabTestAdmin)
admin.site.register(Slide, SlideAdmin)
# admin.site.register(Test, TestAdmin)  # Commented out - Test model not in use
admin.site.register(UserProgress, UserProgressAdmin)
admin.site.register(UserObservation, UserObservationAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)  # Temporarily disabled - table doesn't exist

# تنظیمات ظاهری پنل ادمین
admin.site.site_header = "پنل مدیریت Heyvoonak"
admin.site.site_title = "مدیریت Heyvoonak"
admin.site.index_title = "خوش آمدید به پنل مدیریت Heyvoonak"