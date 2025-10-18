"""
دستور مدیریتی Django برای پاکسازی کش
استفاده: python manage.py clear_cache
"""

from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'پاکسازی کامل کش Django'

    def handle(self, *args, **options):
        try:
            cache.clear()
            self.stdout.write(
                self.style.SUCCESS('✅ کش با موفقیت پاک شد!')
            )
            
            # نمایش اطلاعات اضافی
            self.stdout.write(
                self.style.WARNING('\n📝 توجه:')
            )
            self.stdout.write(
                '- کش Django پاک شد'
            )
            self.stdout.write(
                '- برای پاکسازی کامل، مرورگر خود را هم رفرش کنید (Ctrl+F5)'
            )
            self.stdout.write(
                '- برای پاکسازی session ها: python manage.py clearsessions'
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ خطا در پاکسازی کش: {str(e)}')
            )


