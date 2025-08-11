from django.core.management.base import BaseCommand
from cases.models import Case, LabTest, Test, Slide, CaseCategory


class Command(BaseCommand):
    help = 'اضافه کردن تست‌ها و مشاهدات به تمام کیس‌های موجود'

    def handle(self, *args, **options):
        # ایجاد دسته‌بندی اگر موجود نباشد
        category, created = CaseCategory.objects.get_or_create(
            name="بیماری‌های داخلی",
            slug="internal-diseases",
            defaults={'description': 'کیس‌های مربوط به بیماری‌های داخلی دام'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'دسته‌بندی "{category.name}" ایجاد شد'))
        
        # دریافت تمام کیس‌ها
        cases = Case.objects.all()
        
        for case in cases:
            self.stdout.write(f'در حال پردازش کیس: {case.title} (ID: {case.id})')
            
            # اگر کیس دسته‌بندی ندارد، دسته‌بندی پیش‌فرض را اضافه کن
            if not case.category:
                case.category = category
                case.save()
                self.stdout.write(f'  دسته‌بندی به کیس اضافه شد')
            
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
            Test.objects.create(
                case=case,
                title='cbc',
                report='نتایج CBC نشان‌دهنده کم‌خونی و افزایش تعداد گلبول‌های سفید است',
                observations=['کم‌خونی', 'افزایش WBC', 'کاهش RBC', 'کاهش HGB', 'کاهش HCT'],
                correct_observations=['کم‌خونی', 'افزایش WBC', 'کاهش RBC', 'کاهش HGB', 'کاهش HCT']
            )
            
            # ایجاد مشاهدات شیمی بالینی
            Test.objects.create(
                case=case,
                title='chem',
                report='نتایج شیمی بالینی نشان‌دهنده آسیب کبدی است',
                observations=['افزایش ALT', 'افزایش AST', 'افزایش ALP', 'افزایش بیلی‌روبین', 'افزایش BUN'],
                correct_observations=['افزایش ALT', 'افزایش AST', 'افزایش ALP', 'افزایش بیلی‌روبین', 'افزایش BUN']
            )
            
            # ایجاد مشاهدات تست‌های دیگر
            Test.objects.create(
                case=case,
                title='other',
                report='سایر تست‌ها نشان‌دهنده اختلالات متابولیک است',
                observations=['افزایش BUN', 'افزایش کراتینین', 'قند خون طبیعی', 'اختلال عملکرد کلیه'],
                correct_observations=['افزایش BUN', 'افزایش کراتینین', 'قند خون طبیعی', 'اختلال عملکرد کلیه']
            )
            
            # ایجاد مشاهدات اسلاید
            Test.objects.create(
                case=case,
                title='slide',
                report='اسلایدهای بافت کبد نشان‌دهنده التهاب و تخریب سلولی است',
                observations=['التهاب کبد', 'تخریب سلولی', 'فیبروز', 'نکروز', 'تجمع سلول‌های التهابی'],
                correct_observations=['التهاب کبد', 'تخریب سلولی', 'فیبروز', 'نکروز', 'تجمع سلول‌های التهابی']
            )
            
            # ایجاد اسلاید نمونه (بدون تصویر)
            Slide.objects.create(
                case=case,
                description='اسلاید بافت کبد - التهاب مزمن با فیبروز'
            )
            
            self.stdout.write(f'  ✅ تست‌ها و مشاهدات اضافه شد')
        
        self.stdout.write(self.style.SUCCESS(f'تمام {cases.count()} کیس با موفقیت بروزرسانی شدند')) 