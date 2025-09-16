from django.core.management.base import BaseCommand
from cases.models import Case, CaseTest, CaseOption, TEST_TYPES, CBC_DEFAULT_OPTIONS, CHEM_DEFAULT_OPTIONS, MORPHO_DEFAULT_OPTIONS


class Command(BaseCommand):
    help = 'ایجاد تست‌های پیش‌فرض برای کیس‌ها'

    def add_arguments(self, parser):
        parser.add_argument('--case-id', type=int, help='ID کیس خاص (اختیاری)')

    def handle(self, *args, **options):
        if options['case_id']:
            cases = Case.objects.filter(id=options['case_id'])
        else:
            cases = Case.objects.all()

        for case in cases:
            self.stdout.write(f'ایجاد تست‌های پیش‌فرض برای کیس: {case.title}')
            
            # ایجاد تست CBC
            cbc_test, created = CaseTest.objects.get_or_create(
                case=case,
                test_category='CBC',
                defaults={
                    'question': 'نتایج آزمایش CBC را بررسی کنید:',
                    'type': 'multiple_choice',
                    'order_index': 1
                }
            )
            if created:
                self.create_test_options(cbc_test, CBC_DEFAULT_OPTIONS, 'CBC')
                self.stdout.write(f'  ✅ تست CBC ایجاد شد')

            # ایجاد تست Clinical Chemistry
            chem_test, created = CaseTest.objects.get_or_create(
                case=case,
                test_category='CHEM',
                defaults={
                    'question': 'نتایج آزمایش شیمی بالینی را بررسی کنید:',
                    'type': 'multiple_choice',
                    'order_index': 2
                }
            )
            if created:
                self.create_test_options(chem_test, CHEM_DEFAULT_OPTIONS, 'CHEM')
                self.stdout.write(f'  ✅ تست Clinical Chemistry ایجاد شد')

            # ایجاد تست Morphological Changes
            morpho_test, created = CaseTest.objects.get_or_create(
                case=case,
                test_category='MORPHO',
                defaults={
                    'question': 'تغییرات مورفولوژیک را بررسی کنید:',
                    'type': 'multiple_choice',
                    'order_index': 3
                }
            )
            if created:
                self.create_test_options(morpho_test, MORPHO_DEFAULT_OPTIONS, 'MORPHO')
                self.stdout.write(f'  ✅ تست Morphological Changes ایجاد شد')

        self.stdout.write(self.style.SUCCESS('✅ تست‌های پیش‌فرض با موفقیت ایجاد شدند!'))

    def create_test_options(self, test, options_list, test_type):
        """ایجاد گزینه‌های تست"""
        for i, option_text in enumerate(options_list):
            CaseOption.objects.create(
                test=test,
                option_text=option_text,
                is_correct=False,  # پیش‌فرض همه غلط هستند
                order_index=i
            )
