"""
دستور مدیریتی Django برای نمایش تنظیمات فعلی
استفاده: python manage.py show_config
"""

from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'نمایش تنظیمات فعلی از .env و settings.py'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS('⚙️  تنظیمات فعلی سیستم'))
        self.stdout.write("=" * 70)
        
        # تنظیمات اصلی Django
        self.stdout.write(self.style.HTTP_INFO('\n📌 تنظیمات اصلی:'))
        self.stdout.write("-" * 70)
        self.print_setting('DEBUG', settings.DEBUG)
        self.print_setting('SECRET_KEY', self.mask_secret(settings.SECRET_KEY))
        self.print_setting('ALLOWED_HOSTS', settings.ALLOWED_HOSTS)
        
        # تنظیمات دیتابیس
        self.stdout.write(self.style.HTTP_INFO('\n🗄️  تنظیمات دیتابیس:'))
        self.stdout.write("-" * 70)
        db_settings = settings.DATABASES.get('default', {})
        self.print_setting('Engine', db_settings.get('ENGINE', 'N/A'))
        self.print_setting('Name', db_settings.get('NAME', 'N/A'))
        self.print_setting('Host', db_settings.get('HOST', 'N/A'))
        self.print_setting('Port', db_settings.get('PORT', 'N/A'))
        self.print_setting('User', db_settings.get('USER', 'N/A'))
        
        # تنظیمات Cache
        self.stdout.write(self.style.HTTP_INFO('\n💾 تنظیمات Cache:'))
        self.stdout.write("-" * 70)
        cache_settings = settings.CACHES.get('default', {})
        self.print_setting('Backend', cache_settings.get('BACKEND', 'N/A'))
        self.print_setting('Timeout', f"{cache_settings.get('TIMEOUT', 'N/A')} ثانیه")
        
        # تنظیمات Session
        self.stdout.write(self.style.HTTP_INFO('\n🔐 تنظیمات Session:'))
        self.stdout.write("-" * 70)
        self.print_setting('Engine', settings.SESSION_ENGINE)
        self.print_setting('Cookie Age', f"{settings.SESSION_COOKIE_AGE} ثانیه ({settings.SESSION_COOKIE_AGE // 3600} ساعت)")
        
        # تنظیمات Static و Media
        self.stdout.write(self.style.HTTP_INFO('\n📁 تنظیمات Static و Media:'))
        self.stdout.write("-" * 70)
        self.print_setting('STATIC_URL', settings.STATIC_URL)
        self.print_setting('STATIC_ROOT', settings.STATIC_ROOT)
        self.print_setting('MEDIA_URL', settings.MEDIA_URL)
        self.print_setting('MEDIA_ROOT', settings.MEDIA_ROOT)
        self.print_setting('STATICFILES_STORAGE', settings.STATICFILES_STORAGE)
        
        # متغیرهای محیطی
        self.stdout.write(self.style.HTTP_INFO('\n🌍 متغیرهای محیطی (.env):'))
        self.stdout.write("-" * 70)
        env_vars = [
            'DEBUG', 'SECRET_KEY', 'DB_ENGINE', 'DB_NAME', 'USE_SQLITE',
            'VERCEL', 'VERCEL_DOMAIN', 'ALLOW_ALL_HOSTS',
            'CACHE_TIMEOUT', 'SESSION_COOKIE_AGE', 'LOG_LEVEL'
        ]
        for var in env_vars:
            value = os.getenv(var, 'تنظیم نشده')
            if 'SECRET' in var or 'PASSWORD' in var:
                value = self.mask_secret(str(value))
            self.print_setting(var, value)
        
        # Middleware
        self.stdout.write(self.style.HTTP_INFO('\n🛡️  Middleware فعال:'))
        self.stdout.write("-" * 70)
        for i, middleware in enumerate(settings.MIDDLEWARE, 1):
            short_name = middleware.split('.')[-1]
            status = '✅' if 'whitenoise' in middleware.lower() or 'nocache' in middleware.lower() else '  '
            self.stdout.write(f"{status} {i}. {short_name}")
            if i <= 3:  # نمایش مسیر کامل فقط برای 3 اولی
                self.stdout.write(f"     {self.style.WARNING(middleware)}")
        
        # Installed Apps (فقط custom apps)
        self.stdout.write(self.style.HTTP_INFO('\n📦 اپلیکیشن‌های سفارشی:'))
        self.stdout.write("-" * 70)
        custom_apps = [app for app in settings.INSTALLED_APPS 
                      if not app.startswith('django.') and not app.startswith('rest_framework')]
        for app in custom_apps:
            self.stdout.write(f"  • {app}")
        
        # بررسی وضعیت
        self.stdout.write(self.style.HTTP_INFO('\n🔍 بررسی وضعیت:'))
        self.stdout.write("-" * 70)
        
        # بررسی DEBUG
        if settings.DEBUG:
            self.stdout.write(self.style.WARNING('⚠️  DEBUG=True - مناسب فقط برای توسعه'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ DEBUG=False - آماده برای production'))
        
        # بررسی SECRET_KEY
        if settings.SECRET_KEY == 'django-insecure-REPLACED-FOR-SECURITY':
            self.stdout.write(self.style.ERROR('❌ SECRET_KEY پیش‌فرض است - حتماً تغییر دهید!'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ SECRET_KEY سفارشی است'))
        
        # بررسی ALLOWED_HOSTS
        if '*' in settings.ALLOWED_HOSTS:
            self.stdout.write(self.style.WARNING('⚠️  ALLOWED_HOSTS شامل * است - در production تغییر دهید'))
        elif settings.ALLOWED_HOSTS:
            self.stdout.write(self.style.SUCCESS(f'✅ ALLOWED_HOSTS تنظیم شده ({len(settings.ALLOWED_HOSTS)} host)'))
        
        # بررسی WhiteNoise
        has_whitenoise = any('whitenoise' in m.lower() for m in settings.MIDDLEWARE)
        if has_whitenoise:
            self.stdout.write(self.style.SUCCESS('✅ WhiteNoise فعال است'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  WhiteNoise غیرفعال است'))
        
        # بررسی NoCacheMiddleware
        has_nocache = any('nocache' in m.lower() for m in settings.MIDDLEWARE)
        if has_nocache:
            self.stdout.write(self.style.SUCCESS('✅ NoCacheMiddleware فعال است'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  NoCacheMiddleware غیرفعال است'))
        
        # بررسی فایل .env
        from pathlib import Path
        env_file = Path('.env')
        if env_file.exists():
            self.stdout.write(self.style.SUCCESS('✅ فایل .env وجود دارد'))
        else:
            self.stdout.write(self.style.ERROR('❌ فایل .env وجود ندارد'))
            self.stdout.write(self.style.WARNING('   برای ایجاد: python create_env.py'))
        
        # پیشنهادات
        self.stdout.write(self.style.HTTP_INFO('\n💡 پیشنهادات:'))
        self.stdout.write("-" * 70)
        
        if settings.DEBUG:
            self.stdout.write('• برای تست production: DEBUG=False python manage.py runserver')
        
        if not has_whitenoise:
            self.stdout.write('• برای serve کردن static files در DEBUG=False، WhiteNoise را اضافه کنید')
        
        cache_timeout = settings.CACHES.get('default', {}).get('TIMEOUT', 0)
        if cache_timeout == 0:
            self.stdout.write('• Cache غیرفعال است - برای بهبود performance فعال کنید')
        
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS('✅ اطلاعات نمایش داده شد'))
        self.stdout.write("=" * 70)
    
    def print_setting(self, name, value):
        """چاپ یک تنظیم"""
        name_formatted = f"{name}:"
        self.stdout.write(f"  {name_formatted:25} {self.style.WARNING(str(value))}")
    
    def mask_secret(self, value):
        """مخفی کردن مقادیر حساس"""
        if not value or value == 'N/A':
            return value
        value_str = str(value)
        if len(value_str) <= 8:
            return '*' * len(value_str)
        return value_str[:4] + '*' * (len(value_str) - 8) + value_str[-4:]

