#!/usr/bin/env python3
"""
اسکریپت بررسی امنیت پروژه Django
این اسکریپت تنظیمات امنیتی پروژه را بررسی می‌کند
"""

import os
import re
from pathlib import Path

def check_debug_mode():
    """بررسی وضعیت DEBUG"""
    print("🔍 بررسی وضعیت DEBUG...")
    
    settings_file = Path("vetlms/settings.py")
    if settings_file.exists():
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        debug_match = re.search(r'DEBUG\s*=\s*(True|False)', content)
        if debug_match:
            debug_value = debug_match.group(1)
            if debug_value == 'False':
                print("✅ DEBUG = False (امن)")
            else:
                print("❌ DEBUG = True (نامن)")
        else:
            print("⚠️  DEBUG تنظیم نشده")
    else:
        print("❌ فایل settings.py یافت نشد")

def check_secret_key():
    """بررسی SECRET_KEY"""
    print("\n🔑 بررسی SECRET_KEY...")
    
    settings_file = Path("vetlms/settings.py")
    if settings_file.exists():
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        secret_match = re.search(r'SECRET_KEY\s*=\s*[\'"]([^\'"]+)[\'"]', content)
        if secret_match:
            secret_key = secret_match.group(1)
            if 'django-insecure-' in secret_key:
                print("⚠️  SECRET_KEY پیش‌فرض است - باید تغییر کند")
            elif len(secret_key) < 20:
                print("❌ SECRET_KEY خیلی کوتاه است")
            else:
                print("✅ SECRET_KEY مناسب است")
        else:
            print("❌ SECRET_KEY یافت نشد")

def check_allowed_hosts():
    """بررسی ALLOWED_HOSTS"""
    print("\n🌐 بررسی ALLOWED_HOSTS...")
    
    settings_file = Path("vetlms/settings.py")
    if settings_file.exists():
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        hosts_match = re.search(r'ALLOWED_HOSTS\s*=\s*\[([^\]]+)\]', content)
        if hosts_match:
            hosts = hosts_match.group(1)
            if '*' in hosts:
                print("❌ ALLOWED_HOSTS شامل * است (نامن)")
            else:
                print("✅ ALLOWED_HOSTS محدود است")
        else:
            print("⚠️  ALLOWED_HOSTS یافت نشد")

def check_security_middleware():
    """بررسی middleware های امنیتی"""
    print("\n🛡️  بررسی middleware های امنیتی...")
    
    settings_file = Path("vetlms/settings.py")
    if settings_file.exists():
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        security_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware'
        ]
        
        for middleware in security_middleware:
            if middleware in content:
                print(f"✅ {middleware} فعال است")
            else:
                print(f"❌ {middleware} فعال نیست")

def check_error_templates():
    """بررسی فایل‌های خطا"""
    print("\n📄 بررسی فایل‌های خطا...")
    
    error_templates = ['404.html', '500.html', '403.html']
    templates_dir = Path("templates")
    
    if templates_dir.exists():
        for template in error_templates:
            template_file = templates_dir / template
            if template_file.exists():
                print(f"✅ {template} موجود است")
            else:
                print(f"❌ {template} موجود نیست")
    else:
        print("❌ پوشه templates یافت نشد")

def check_logging():
    """بررسی تنظیمات logging"""
    print("\n📝 بررسی تنظیمات logging...")
    
    settings_file = Path("vetlms/settings.py")
    if settings_file.exists():
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'LOGGING' in content:
            print("✅ تنظیمات logging موجود است")
        else:
            print("⚠️  تنظیمات logging موجود نیست")

def check_static_files():
    """بررسی فایل‌های static"""
    print("\n📁 بررسی فایل‌های static...")
    
    static_dir = Path("static")
    if static_dir.exists():
        print("✅ پوشه static موجود است")
    else:
        print("⚠️  پوشه static موجود نیست")

def check_media_files():
    """بررسی فایل‌های media"""
    print("\n🖼️  بررسی فایل‌های media...")
    
    media_dir = Path("media")
    if media_dir.exists():
        print("✅ پوشه media موجود است")
    else:
        print("⚠️  پوشه media موجود نیست")

def main():
    """تابع اصلی"""
    print("🔒 بررسی امنیت پروژه Django")
    print("=" * 50)
    
    check_debug_mode()
    check_secret_key()
    check_allowed_hosts()
    check_security_middleware()
    check_error_templates()
    check_logging()
    check_static_files()
    check_media_files()
    
    print("\n" + "=" * 50)
    print("✅ بررسی امنیت کامل شد")
    print("\n💡 توصیه‌های امنیتی:")
    print("1. DEBUG را در production روی False قرار دهید")
    print("2. SECRET_KEY قوی و منحصر به فرد استفاده کنید")
    print("3. ALLOWED_HOSTS را محدود کنید")
    print("4. از HTTPS در production استفاده کنید")
    print("5. فایل‌های حساس را در .gitignore قرار دهید")

if __name__ == "__main__":
    main() 