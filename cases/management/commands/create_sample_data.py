from django.core.management.base import BaseCommand
from cases.models import CaseCategory, SubCategory, Case


class Command(BaseCommand):
    help = 'ایجاد داده‌های نمونه برای دسته‌بندی‌ها و زیردسته‌بندی‌ها'

    def handle(self, *args, **options):
        # ایجاد دسته‌بندی‌های اصلی
        categories_data = [
            {'name': 'بیماری‌های داخلی', 'slug': 'internal-diseases'},
            {'name': 'جراحی', 'slug': 'surgery'},
            {'name': 'زنان و زایمان', 'slug': 'gynecology'},
            {'name': 'اطفال', 'slug': 'pediatrics'},
            {'name': 'روانپزشکی', 'slug': 'psychiatry'},
        ]
        
        for cat_data in categories_data:
            category, created = CaseCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            if created:
                self.stdout.write(f'دسته‌بندی "{category.name}" ایجاد شد')
            else:
                self.stdout.write(f'دسته‌بندی "{category.name}" از قبل وجود دارد')

        # ایجاد زیردسته‌بندی‌ها
        subcategories_data = [
            {'name': 'بیماری‌های قلبی', 'category_slug': 'internal-diseases'},
            {'name': 'بیماری‌های گوارشی', 'category_slug': 'internal-diseases'},
            {'name': 'بیماری‌های تنفسی', 'category_slug': 'internal-diseases'},
            {'name': 'جراحی عمومی', 'category_slug': 'surgery'},
            {'name': 'جراحی قلب', 'category_slug': 'surgery'},
            {'name': 'جراحی مغز و اعصاب', 'category_slug': 'surgery'},
            {'name': 'زایمان طبیعی', 'category_slug': 'gynecology'},
            {'name': 'سزارین', 'category_slug': 'gynecology'},
            {'name': 'بیماری‌های نوزادان', 'category_slug': 'pediatrics'},
            {'name': 'بیماری‌های کودکان', 'category_slug': 'pediatrics'},
        ]
        
        for sub_data in subcategories_data:
            try:
                category = CaseCategory.objects.get(slug=sub_data['category_slug'])
                subcategory, created = SubCategory.objects.get_or_create(
                    name=sub_data['name'],
                    category=category,
                    defaults={'slug': sub_data['name'].lower().replace(' ', '-')}
                )
                if created:
                    self.stdout.write(f'زیردسته‌بندی "{subcategory.name}" ایجاد شد')
                else:
                    self.stdout.write(f'زیردسته‌بندی "{subcategory.name}" از قبل وجود دارد')
            except CaseCategory.DoesNotExist:
                self.stdout.write(f'دسته‌بندی با slug "{sub_data["category_slug"]}" یافت نشد')

        self.stdout.write(
            self.style.SUCCESS('داده‌های نمونه با موفقیت ایجاد شدند')
        )
