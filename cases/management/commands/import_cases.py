from django.core.management.base import BaseCommand
from django.db import transaction
import pandas as pd
from cases.models import Case


class Command(BaseCommand):
    help = 'ایمپورت دسته‌ای کیس‌ها از فایل اکسل'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='مسیر فایل اکسل')
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='تعداد کیس‌ها در هر دسته (پیش‌فرض: 1000)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='فقط نمایش دهد بدون ایجاد کیس‌ها'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        batch_size = options['batch_size']
        dry_run = options['dry_run']

        try:
            self.stdout.write(f'📖 در حال خواندن فایل: {file_path}')
            
            # خواندن فایل اکسل
            if file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                self.stdout.write(self.style.ERROR('فقط فایل‌های .xlsx و .csv پشتیبانی می‌شوند.'))
                return

            # بررسی ستون‌های مورد نیاز
            required_columns = ['title', 'history', 'correct_diagnosis', 'explanation']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                self.stdout.write(
                    self.style.ERROR(f'ستون‌های زیر در فایل موجود نیست: {", ".join(missing_columns)}')
                )
                return

            # پاک کردن ردیف‌های خالی
            df = df.dropna(subset=['title', 'history', 'correct_diagnosis', 'explanation'])
            
            self.stdout.write(f'📊 تعداد ردیف‌های معتبر: {len(df)}')

            if dry_run:
                self.stdout.write('🔍 حالت نمایش (بدون ایجاد کیس‌ها)')
                for index, row in df.head(5).iterrows():
                    self.stdout.write(f'  - {row["title"]}: {row["history"][:50]}...')
                return

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
                    self.stdout.write(
                        self.style.WARNING(f'خطا در پردازش ردیف {index+1}: {str(e)}')
                    )

            # ایجاد کیس‌ها به صورت دسته‌ای
            total_created = 0
            
            with transaction.atomic():
                for i in range(0, len(cases_to_create), batch_size):
                    batch = cases_to_create[i:i + batch_size]
                    try:
                        created_cases = Case.objects.bulk_create(batch, ignore_conflicts=True)
                        total_created += len(created_cases)
                        
                        # نمایش پیشرفت
                        progress = min((i + batch_size) / len(cases_to_create) * 100, 100)
                        self.stdout.write(
                            f'📈 پیشرفت: {progress:.1f}% - {total_created} کیس ایجاد شد'
                        )
                        
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'خطا در ایجاد دسته {i//batch_size + 1}: {str(e)}')
                        )

            self.stdout.write(
                self.style.SUCCESS(f'✅ {total_created} کیس با موفقیت ایجاد شد.')
            )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'فایل {file_path} پیدا نشد.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'خطا در پردازش فایل: {str(e)}')) 