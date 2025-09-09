from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
import pandas as pd
from .models import Case, LabTest, Slide, Test, TestOption, UserProgress, UserObservation, UserProfile, CaseCategory


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(
        label='فایل اکسل را انتخاب کنید',
        help_text='فایل باید شامل ستون‌های: title, history, correct_diagnosis, explanation باشد'
    )


class SimpleCaseImportForm(forms.Form):
    title = forms.CharField(max_length=200, label='عنوان کیس')
    history = forms.CharField(widget=forms.Textarea, label='پیشینه کیس')
    correct_diagnosis = forms.CharField(widget=forms.Textarea, label='تشخیص صحیح')
    explanation = forms.CharField(widget=forms.Textarea, label='توضیحات')


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
    extra = 2
    fields = ('test_type', 'name', 'reference_range', 'value', 'report')
    classes = ('collapse',)


class TestInline(admin.StackedInline):
    model = Test
    extra = 1
    classes = ('collapse',)
    fields = ('title', 'report', 'observations', 'correct_observations')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # اضافه کردن help_text برای فیلدهای JSON
        form.base_fields['observations'].help_text = 'لیست گزینه‌های مشاهدات را به صورت JSON وارد کنید. مثال: ["گزینه 1", "گزینه 2", "گزینه 3"]'
        form.base_fields['correct_observations'].help_text = 'لیست گزینه‌های صحیح را به صورت JSON وارد کنید. مثال: ["گزینه صحیح 1", "گزینه صحیح 2"]'
        
        return form


@admin.action(description="ساخت کپی از کیس‌های انتخاب‌شده")
def duplicate_cases(modeladmin, request, queryset):
    for obj in queryset:
        labtests = list(obj.lab_tests.all())
        slides = list(obj.slides.all())
        tests = list(obj.tests.all())

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
        for tst in tests:
            tst.pk = None
            tst.case = obj
            tst.save()


@admin.action(description="اضافه کردن تست‌ها و مشاهدات به کیس‌های انتخاب‌شده")
def add_tests_to_cases(modeladmin, request, queryset):
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
                    LabTest.objects.create(case=case, **test_data)
            
            # بررسی اینکه آیا مشاهدات قبلاً وجود دارند
            if case.tests.count() == 0:
                # ایجاد مشاهدات CBC
                Test.objects.create(
                    case=case,
                    title='cbc',
                    report='نتایج آزمایش CBC نشان‌دهنده تغییرات خفیف است. هموگلوبین در حد طبیعی و WBC کمی افزایش یافته است.',
                    observations=['افزایش تعداد گلبول‌های سفید', 'کاهش هموگلوبین', 'افزایش قند خون', 'التهاب در بافت', 'وجود پروتئین در ادرار', 'کاهش پلاکت‌ها'],
                    correct_observations=['افزایش تعداد گلبول‌های سفید', 'التهاب در بافت']
                )
                
                # ایجاد مشاهدات CHEM
                Test.objects.create(
                    case=case,
                    title='chem',
                    report='نتایج شیمی بالینی نشان‌دهنده قند خون طبیعی است.',
                    observations=['افزایش قند خون', 'کاهش قند خون', 'قند خون طبیعی', 'اختلال در متابولیسم'],
                    correct_observations=['قند خون طبیعی']
                )
                
                # ایجاد مشاهدات OTHER
                Test.objects.create(
                    case=case,
                    title='other',
                    report='تست ادرار نشان‌دهنده وجود پروتئین است.',
                    observations=['ادرار طبیعی', 'وجود پروتئین', 'وجود خون', 'وجود قند'],
                    correct_observations=['وجود پروتئین']
                )
                
                # ایجاد مشاهدات SLIDE
                Test.objects.create(
                    case=case,
                    title='slide',
                    report='اسلاید میکروسکوپی نشان‌دهنده تغییرات سلولی است.',
                    observations=['سلول‌های طبیعی', 'تغییرات سلولی', 'التهاب', 'نکروز'],
                    correct_observations=['تغییرات سلولی', 'التهاب']
                )
                
        except Exception as e:
            messages.error(request, f'خطا در اضافه کردن تست‌ها به کیس "{case.title}": {str(e)}')
    
    messages.success(request, f'تست‌ها و مشاهدات به {queryset.count()} کیس اضافه شدند.')


class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'lab_tests_count', 'slides_count', 'created_at')
    search_fields = ('title', 'history', 'correct_diagnosis')
    list_filter = ('category', 'created_at',)
    actions = [duplicate_cases, add_tests_to_cases]
    inlines = [LabTestInline, SlideInline, TestInline]
    change_list_template = 'admin/cases/case/change_list.html'
    
    # اضافه کردن فیلدهای ساده برای ایجاد کیس
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
            path('import-excel/', self.admin_site.admin_view(self.import_excel_view), name='cases_case_import_excel'),
            path('add-simple/', self.admin_site.admin_view(self.add_simple_case_view), name='cases_case_add_simple'),
        ]
        return custom_urls + urls

    def add_simple_case_view(self, request):
        if request.method == 'POST':
            form = SimpleCaseImportForm(request.POST)
            if form.is_valid():
                try:
                    # ایجاد کیس جدید
                    case = Case.objects.create(
                        title=form.cleaned_data['title'],
                        history=form.cleaned_data['history'],
                        correct_diagnosis=form.cleaned_data['correct_diagnosis'],
                        explanation=form.cleaned_data['explanation']
                    )
                    
                    messages.info(request, f'کیس "{case.title}" ایجاد شد. در حال اضافه کردن تست‌ها...')
                    
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
                    
                    lab_tests_created = 0
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
                    
                    # ایجاد مشاهدات نمونه
                    sample_observations = [
                        'افزایش تعداد گلبول‌های سفید',
                        'کاهش هموگلوبین',
                        'افزایش قند خون',
                        'التهاب در بافت',
                        'وجود پروتئین در ادرار',
                        'کاهش پلاکت‌ها'
                    ]
                    
                    try:
                        Test.objects.create(
                            case=case,
                            title='cbc',
                            report='نتایج آزمایش CBC نشان‌دهنده تغییرات خفیف است. هموگلوبین در حد طبیعی و WBC کمی افزایش یافته است.',
                            observations=sample_observations,
                            correct_observations=['افزایش تعداد گلبول‌های سفید', 'التهاب در بافت']
                        )
                        messages.info(request, 'مشاهدات CBC ایجاد شد.')
                    except Exception as e:
                        messages.warning(request, f'خطا در ایجاد مشاهدات CBC: {str(e)}')
                    
                    try:
                        Test.objects.create(
                            case=case,
                            title='chem',
                            report='نتایج شیمی بالینی نشان‌دهنده قند خون طبیعی است.',
                            observations=['افزایش قند خون', 'کاهش قند خون', 'قند خون طبیعی', 'اختلال در متابولیسم'],
                            correct_observations=['قند خون طبیعی']
                        )
                        messages.info(request, 'مشاهدات CHEM ایجاد شد.')
                    except Exception as e:
                        messages.warning(request, f'خطا در ایجاد مشاهدات CHEM: {str(e)}')
                    
                    try:
                        Test.objects.create(
                            case=case,
                            title='other',
                            report='تست ادرار نشان‌دهنده وجود پروتئین است.',
                            observations=['ادرار طبیعی', 'وجود پروتئین', 'وجود خون', 'وجود قند'],
                            correct_observations=['وجود پروتئین']
                        )
                        messages.info(request, 'مشاهدات OTHER ایجاد شد.')
                    except Exception as e:
                        messages.warning(request, f'خطا در ایجاد مشاهدات OTHER: {str(e)}')
                    
                    # ایجاد اسلاید نمونه
                    try:
                        Test.objects.create(
                            case=case,
                            title='slide',
                            report='اسلاید میکروسکوپی نشان‌دهنده تغییرات سلولی است.',
                            observations=['سلول‌های طبیعی', 'تغییرات سلولی', 'التهاب', 'نکروز'],
                            correct_observations=['تغییرات سلولی', 'التهاب']
                        )
                        messages.info(request, 'مشاهدات SLIDE ایجاد شد.')
                    except Exception as e:
                        messages.warning(request, f'خطا در ایجاد مشاهدات SLIDE: {str(e)}')
                    
                    messages.success(request, f'کیس "{case.title}" با موفقیت ایجاد شد!')
                    messages.success(request, f'تست‌ها: {lab_tests_created} عدد | مشاهدات: 4 نوع')
                    
                    return HttpResponseRedirect('../')
                    
                except Exception as e:
                    messages.error(request, f'خطا در ایجاد کیس: {str(e)}')
                    import traceback
                    messages.error(request, f'جزئیات خطا: {traceback.format_exc()}')
        else:
            form = SimpleCaseImportForm()
        
        context = {
            'form': form,
            'title': 'افزودن کیس جدید',
            'opts': self.model._meta,
        }
        return render(request, 'admin/cases/case/add_simple.html', context)

    def import_excel_view(self, request):
        if request.method == 'POST':
            form = ExcelImportForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    excel_file = request.FILES['excel_file']
                    
                    # خواندن فایل اکسل
                    if excel_file.name.endswith('.xlsx'):
                        df = pd.read_excel(excel_file)
                    elif excel_file.name.endswith('.csv'):
                        df = pd.read_csv(excel_file)
                    else:
                        messages.error(request, 'فقط فایل‌های .xlsx و .csv پشتیبانی می‌شوند.')
                        return HttpResponseRedirect('../')
                    
                    # بررسی ستون‌های مورد نیاز
                    required_columns = ['title', 'history', 'correct_diagnosis', 'explanation']
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    
                    if missing_columns:
                        messages.error(request, f'ستون‌های زیر در فایل موجود نیست: {", ".join(missing_columns)}')
                        return HttpResponseRedirect('../')
                    
                    # پاک کردن ردیف‌های خالی
                    df = df.dropna(subset=['title', 'history', 'correct_diagnosis', 'explanation'])
                    
                    # تبدیل به لیست برای bulk_create
                    cases_to_create = []
                    for index, row in df.iterrows():
                        try:
                            case = Case(
                                title=str(row['title']).strip(),
                                history=str(row['history']).strip(),
                                correct_diagnosis=str(row['correct_diagnosis']).strip(),
                                explanation=str(row['explanation']).strip()
                            )
                            cases_to_create.append(case)
                        except Exception as e:
                            messages.warning(request, f'خطا در پردازش ردیف {index+1}: {str(e)}')
                    
                    # ایجاد کیس‌ها به صورت دسته‌ای (batch)
                    batch_size = 1000  # تعداد کیس‌ها در هر دسته
                    total_created = 0
                    
                    for i in range(0, len(cases_to_create), batch_size):
                        batch = cases_to_create[i:i + batch_size]
                        try:
                            created_cases = Case.objects.bulk_create(batch, ignore_conflicts=True)
                            total_created += len(created_cases)
                            
                            # نمایش پیشرفت
                            progress = min((i + batch_size) / len(cases_to_create) * 100, 100)
                            messages.info(request, f'پیشرفت: {progress:.1f}% - {total_created} کیس ایجاد شد')
                            
                        except Exception as e:
                            messages.error(request, f'خطا در ایجاد دسته {i//batch_size + 1}: {str(e)}')
                    
                    messages.success(request, f'{total_created} کیس با موفقیت ایجاد شد.')
                    return HttpResponseRedirect('../')
                    
                except Exception as e:
                    messages.error(request, f'خطا در پردازش فایل: {str(e)}')
        else:
            form = ExcelImportForm()
        
        context = {
            'form': form,
            'title': 'ورود دسته‌ای کیس‌ها از فایل اکسل',
            'opts': self.model._meta,
        }
        return render(request, 'admin/cases/case/import_excel.html', context)

    def lab_tests_count(self, obj):
        return obj.lab_tests.count()
    lab_tests_count.short_description = "تعداد تست‌ها"

    def slides_count(self, obj):
        return obj.slides.count()
    slides_count.short_description = "تعداد اسلایدها"


class LabTestAdmin(admin.ModelAdmin):
    list_display = ('case', 'test_type', 'name', 'value')
    list_filter = ('test_type',)
    search_fields = ('name', 'report', 'case__title')


class SlideAdmin(admin.ModelAdmin):
    list_display = ('case', 'thumbnail', 'description')
    readonly_fields = ('thumbnail',)

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px; border-radius:4px;" />', obj.image.url)
        return "-"
    thumbnail.short_description = "پیش‌نمایش"


class TestOptionInline(admin.TabularInline):
    model = TestOption
    extra = 1
    fields = ('text', 'is_correct', 'order_index')
    ordering = ('order_index', 'id')

class TestAdmin(admin.ModelAdmin):
    list_display = ('case', 'title', 'options_count', 'correct_options_count')
    list_filter = ('case',)
    search_fields = ('case__title', 'title')
    fields = ('case', 'title', 'report')
    inlines = [TestOptionInline]

    def options_count(self, obj):
        return obj.options.count()
    options_count.short_description = "تعداد گزینه‌ها"

    def correct_options_count(self, obj):
        return obj.options.filter(is_correct=True).count()
    correct_options_count.short_description = "تعداد پاسخ‌های صحیح"


class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'case', 'completed', 'accuracy_percentage', 'is_diagnosis_correct', 'completed_at')
    list_filter = ('completed', 'is_diagnosis_correct')
    search_fields = ('user__username', 'case__title')
    readonly_fields = ('accuracy_percentage',)

class UserObservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'case', 'observation_text', 'is_correct', 'selected_at')
    list_filter = ('is_correct', 'selected_at')
    search_fields = ('user__username', 'case__title', 'observation_text')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'subscription_start',
        'subscription_end',
        'is_subscription_active_admin',
        'overall_accuracy',
        'diagnosis_accuracy',
        'total_cases_completed',
        'last_activity',
    )
    list_filter = (
        'subscription_start',
        'subscription_end',
    )
    search_fields = ('user__username', 'user__email')
    readonly_fields = (
        'overall_accuracy',
        'diagnosis_accuracy',
        'total_cases_completed',
        'total_observations',
        'total_correct_observations',
        'total_diagnoses',
        'total_correct_diagnoses',
        'average_attempts_per_case',
        'is_subscription_active_admin',
    )
    fieldsets = (
        ('کاربر', {
            'fields': ('user',)
        }),
        ('اشتراک', {
            'fields': ('subscription_start', 'subscription_end', 'is_subscription_active_admin'),
        }),
        ('آمار', {
            'fields': (
                'overall_accuracy', 'diagnosis_accuracy', 'total_cases_completed', 'total_observations',
                'total_correct_observations', 'total_diagnoses', 'total_correct_diagnoses', 'average_attempts_per_case'
            )
        }),
        ('سیستمی', {
            'fields': ('last_activity', 'created_at'),
        })
    )

    actions = ['activate_30_days', 'extend_30_days', 'clear_subscription']

    def is_subscription_active_admin(self, obj):
        return obj.is_subscription_active
    is_subscription_active_admin.boolean = True
    is_subscription_active_admin.short_description = 'اشتراک فعال'

    def activate_30_days(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        now = timezone.now()
        updated = 0
        for profile in queryset:
            profile.subscription_start = now
            profile.subscription_end = now + timedelta(days=30)
            profile.save(update_fields=['subscription_start', 'subscription_end'])
            updated += 1
        self.message_user(request, f"{updated} اشتراک برای ۳۰ روز فعال شد.")
    activate_30_days.short_description = 'فعال‌سازی اشتراک ۳۰ روزه'

    def extend_30_days(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        now = timezone.now()
        updated = 0
        for profile in queryset:
            start = profile.subscription_start or now
            end = profile.subscription_end or now
            if end < now:
                # اگر منقضی شده بود از حالا محاسبه شود
                end = now
                start = now
            profile.subscription_start = start
            profile.subscription_end = end + timedelta(days=30)
            profile.save(update_fields=['subscription_start', 'subscription_end'])
            updated += 1
        self.message_user(request, f"{updated} اشتراک ۳۰ روز تمدید شد.")
    extend_30_days.short_description = 'تمدید ۳۰ روزه اشتراک'

    def clear_subscription(self, request, queryset):
        updated = queryset.update(subscription_start=None, subscription_end=None)
        self.message_user(request, f"اشتراک {updated} کاربر پاک شد.")
    clear_subscription.short_description = 'حذف اشتراک'

admin.site.register(Case, CaseAdmin)
admin.site.register(LabTest, LabTestAdmin)
admin.site.register(Slide, SlideAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(UserProgress, UserProgressAdmin)
admin.site.register(UserObservation, UserObservationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CaseCategory)

# تنظیمات ظاهری پنل ادمین
admin.site.site_header = "پنل مدیریت LMS پاتولوژی دامپزشکی"
admin.site.site_title = "مدیریت VetLMS"
admin.site.index_title = "خوش آمدید به پنل مدیریت"
