from django.core.management.base import BaseCommand
from apps.courses.models import Case, LabTest, Test, Slide, CaseCategory, TestOption
from django.core.files.uploadedfile import SimpleUploadedFile

class Command(BaseCommand):
    help = 'ایجاد کیس نمونه با تمام تست‌ها و مشاهدات'

    def handle(self, *args, **options):
        # ایجاد دسته‌بندی اگر موجود نباشد
        category, created = CaseCategory.objects.get_or_create(
            name="بیماری‌های داخلی",
            slug="internal-diseases",
            defaults={'description': 'کیس‌های مربوط به بیماری‌های داخلی دام'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'دسته‌بندی "{category.name}" ایجاد شد'))
        
        # ایجاد کیس نمونه
        case, created = Case.objects.get_or_create(
            title="کیس نمونه - بیماری کبدی",
            defaults={
                'category': category,
                'history': 'سگ 5 ساله با علائم بی‌اشتهایی، استفراغ و زردی پوست',
                'correct_diagnosis': 'هپاتیت مزمن',
                'explanation': 'بر اساس نتایج آزمایشات و علائم بالینی، تشخیص هپاتیت مزمن مطرح است.'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'کیس "{case.title}" ایجاد شد'))
        
        # حذف تست‌های قبلی
        case.lab_tests.all().delete()
        case.tests.all().delete()
        case.slides.all().delete()
        
        # ایجاد تست‌های CBC
        cbc_tests = [
            {'name': 'RBC', 'value': '4.2', 'reference': '5.5-8.5', 'report': 'کاهش تعداد گلبول‌های قرمز'},
            {'name': 'HGB', 'value': '8.5', 'reference': '12-18', 'report': 'کاهش هموگلوبین'},
            {'name': 'HCT', 'value': '25', 'reference': '37-55', 'report': 'کاهش هماتوکریت'},
            {'name': 'WBC', 'value': '15.2', 'reference': '6-17', 'report': 'افزایش تعداد گلبول‌های سفید'},
        ]
        
        for test_data in cbc_tests:
            LabTest.objects.create(
                case=case,
                test_type='CBC',
                name=test_data['name'],
                value=test_data['value'],
                reference_range=test_data['reference'],
                report=test_data['report']
            )
        
        # ایجاد تست‌های شیمی بالینی
        chem_tests = [
            {'name': 'ALT', 'value': '450', 'reference': '10-100', 'report': 'افزایش قابل توجه آنزیم کبدی'},
            {'name': 'AST', 'value': '380', 'reference': '10-50', 'report': 'افزایش آنزیم کبدی'},
            {'name': 'ALP', 'value': '1200', 'reference': '20-150', 'report': 'افزایش آنزیم کبدی'},
            {'name': 'Bilirubin', 'value': '8.5', 'reference': '0.1-0.3', 'report': 'افزایش بیلی‌روبین'},
        ]
        
        for test_data in chem_tests:
            LabTest.objects.create(
                case=case,
                test_type='CHEM',
                name=test_data['name'],
                value=test_data['value'],
                reference_range=test_data['reference'],
                report=test_data['report']
            )
        
        # ایجاد تست‌های دیگر
        other_tests = [
            {'name': 'Glucose', 'value': '85', 'reference': '70-120', 'report': 'قند خون طبیعی'},
            {'name': 'BUN', 'value': '45', 'reference': '7-25', 'report': 'افزایش نیتروژن اوره خون'},
            {'name': 'Creatinine', 'value': '2.1', 'reference': '0.5-1.5', 'report': 'افزایش کراتینین'},
        ]
        
        for test_data in other_tests:
            LabTest.objects.create(
                case=case,
                test_type='OTHER',
                name=test_data['name'],
                value=test_data['value'],
                reference_range=test_data['reference'],
                report=test_data['report']
            )
        
        # ایجاد مشاهدات CBC
        cbc_test = Test.objects.create(
            case=case,
            title='cbc',
            report='نتایج CBC نشان‌دهنده کم‌خونی و افزایش تعداد گلبول‌های سفید است',
            observations=['کم‌خونی', 'افزایش WBC', 'کاهش RBC', 'کاهش HGB', 'کاهش HCT'],
            correct_observations=['کم‌خونی', 'افزایش WBC', 'کاهش RBC', 'کاهش HGB', 'کاهش HCT']
        )
        for idx, text in enumerate(cbc_test.observations or []):
            TestOption.objects.create(test=cbc_test, text=text, is_correct=(text in (cbc_test.correct_observations or [])), order_index=idx)
        
        # ایجاد مشاهدات شیمی بالینی
        chem_test = Test.objects.create(
            case=case,
            title='chem',
            report='نتایج شیمی بالینی نشان‌دهنده آسیب کبدی است',
            observations=['افزایش ALT', 'افزایش AST', 'افزایش ALP', 'افزایش بیلی‌روبین', 'افزایش BUN'],
            correct_observations=['افزایش ALT', 'افزایش AST', 'افزایش ALP', 'افزایش بیلی‌روبین', 'افزایش BUN']
        )
        for idx, text in enumerate(chem_test.observations or []):
            TestOption.objects.create(test=chem_test, text=text, is_correct=(text in (chem_test.correct_observations or [])), order_index=idx)
        
        # ایجاد مشاهدات تست‌های دیگر
        other_test = Test.objects.create(
            case=case,
            title='other',
            report='سایر تست‌ها نشان‌دهنده اختلالات متابولیک است',
            observations=['افزایش BUN', 'افزایش کراتینین', 'قند خون طبیعی', 'اختلال عملکرد کلیه'],
            correct_observations=['افزایش BUN', 'افزایش کراتینین', 'قند خون طبیعی', 'اختلال عملکرد کلیه']
        )
        for idx, text in enumerate(other_test.observations or []):
            TestOption.objects.create(test=other_test, text=text, is_correct=(text in (other_test.correct_observations or [])), order_index=idx)
        
        # ایجاد مشاهدات اسلاید
        slide_test = Test.objects.create(
            case=case,
            title='slide',
            report='اسلایدهای بافت کبد نشان‌دهنده التهاب و تخریب سلولی است',
            observations=['التهاب کبد', 'تخریب سلولی', 'فیبروز', 'نکروز', 'تجمع سلول‌های التهابی'],
            correct_observations=['التهاب کبد', 'تخریب سلولی', 'فیبروز', 'نکروز', 'تجمع سلول‌های التهابی']
        )
        for idx, text in enumerate(slide_test.observations or []):
            TestOption.objects.create(test=slide_test, text=text, is_correct=(text in (slide_test.correct_observations or [])), order_index=idx)
        
        # ایجاد اسلاید نمونه (بدون تصویر)
        Slide.objects.create(
            case=case,
            description='اسلاید بافت کبد - التهاب مزمن با فیبروز'
        )
        
        self.stdout.write(self.style.SUCCESS(f'تمام تست‌ها و مشاهدات برای کیس "{case.title}" ایجاد شد'))
        self.stdout.write(f'ID کیس: {case.id}')
        self.stdout.write(f'تعداد تست‌های CBC: {case.lab_tests.filter(test_type="CBC").count()}')
        self.stdout.write(f'تعداد تست‌های CHEM: {case.lab_tests.filter(test_type="CHEM").count()}')
        self.stdout.write(f'تعداد تست‌های OTHER: {case.lab_tests.filter(test_type="OTHER").count()}')
        self.stdout.write(f'تعداد مشاهدات: {case.tests.count()}')
        self.stdout.write(f'تعداد اسلایدها: {case.slides.count()}') 