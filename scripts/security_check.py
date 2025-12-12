#!/usr/bin/env python
"""
اسکریپت بررسی امنیتی خودکار پروژه VetLMS

استفاده:
    python scripts/security_check.py
"""

import os
import re
from pathlib import Path

class SecurityChecker:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.issues = []
        self.warnings = []
        
    def check_hardcoded_secrets(self):
        """بررسی وجود اطلاعات حساس در کد"""
        print("🔍 بررسی اطلاعات حساس hardcoded...")
        
        patterns = {
            'password': r'PASSWORD\s*=\s*["\'][^"\']+["\']',
            'secret_key': r'SECRET_KEY\s*=\s*["\']django-insecure',
            'api_key': r'API_KEY\s*=\s*["\'][^"\']{20,}["\']',
        }
        
        settings_file = self.base_dir / 'vetlms' / 'settings.py'
        
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                for key, pattern in patterns.items():
                    matches = re.findall(pattern, content)
                    if matches:
                        self.issues.append(f"⚠️ {key} hardcoded یافت شد در settings.py")
    
    def check_debug_mode(self):
        """بررسی حالت DEBUG"""
        print("🔍 بررسی حالت DEBUG...")
        
        if os.environ.get('DEBUG', 'True').lower() == 'true':
            self.warnings.append("⚠️ DEBUG=True است. در production باید False باشد.")
        else:
            print("✅ DEBUG=False")
    
    def check_sql_injection_patterns(self):
        """بررسی الگوهای SQL Injection"""
        print("🔍 بررسی الگوهای SQL Injection...")
        
        dangerous_patterns = [
            (r'\.raw\(', 'استفاده از .raw()'),
            (r'\.extra\(', 'استفاده از .extra()'),
            (r'cursor\.execute\(', 'استفاده از cursor.execute()'),
        ]
        
        found_issues = False
        
        for root, dirs, files in os.walk(self.base_dir / 'apps'):
            # حذف __pycache__ از جستجو
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            content = f.read()
                            
                            for pattern, description in dangerous_patterns:
                                if re.search(pattern, content):
                                    self.issues.append(
                                        f"🔴 {description} در {file_path.relative_to(self.base_dir)}"
                                    )
                                    found_issues = True
                        except Exception as e:
                            pass
        
        if not found_issues:
            print("✅ هیچ الگوی خطرناک SQL یافت نشد")
    
    def check_xss_protection(self):
        """بررسی محافظت XSS در template ها"""
        print("🔍 بررسی محافظت XSS در template ها...")
        
        unsafe_patterns = [
            r'{{\s*\w+\|safe\s*}}',  # استفاده از |safe
            r'{%\s*autoescape\s+off\s*%}',  # غیرفعال کردن autoescape
        ]
        
        found_issues = False
        
        for root, dirs, files in os.walk(self.base_dir / 'apps'):
            for file in files:
                if file.endswith('.html'):
                    file_path = Path(root) / file
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            content = f.read()
                            
                            for pattern in unsafe_patterns:
                                matches = re.findall(pattern, content)
                                if matches:
                                    self.warnings.append(
                                        f"⚠️ استفاده بالقوه ناامن از template tag در {file_path.relative_to(self.base_dir)}"
                                    )
                                    found_issues = True
                        except Exception as e:
                            pass
        
        if not found_issues:
            print("✅ مشکل XSS آشکاری یافت نشد")
    
    def check_env_file(self):
        """بررسی وجود فایل .env"""
        print("🔍 بررسی فایل .env...")
        
        env_file = self.base_dir / '.env'
        gitignore_file = self.base_dir / '.gitignore'
        
        if not env_file.exists():
            self.warnings.append("⚠️ فایل .env وجود ندارد")
        
        if gitignore_file.exists():
            with open(gitignore_file, 'r') as f:
                content = f.read()
                if '.env' not in content:
                    self.issues.append("🔴 .env در .gitignore نیست!")
        else:
            self.issues.append("🔴 فایل .gitignore وجود ندارد!")
    
    def check_allowed_hosts(self):
        """بررسی ALLOWED_HOSTS"""
        print("🔍 بررسی ALLOWED_HOSTS...")
        
        settings_file = self.base_dir / 'vetlms' / 'settings.py'
        
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if "ALLOWED_HOSTS = ['*']" in content:
                    self.issues.append("🔴 ALLOWED_HOSTS=['*'] خطرناک است!")
    
    def check_csrf_settings(self):
        """بررسی تنظیمات CSRF"""
        print("🔍 بررسی تنظیمات CSRF...")
        
        settings_file = self.base_dir / 'vetlms' / 'settings.py'
        
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if 'CSRF_COOKIE_SECURE' not in content:
                    self.warnings.append("⚠️ CSRF_COOKIE_SECURE تنظیم نشده")
                
                if "'django.middleware.csrf.CsrfViewMiddleware'" not in content:
                    self.issues.append("🔴 CSRF Middleware فعال نیست!")
                else:
                    print("✅ CSRF Middleware فعال است")
    
    def run_all_checks(self):
        """اجرای تمام بررسی‌ها"""
        print("\n" + "="*60)
        print("🔒 بررسی امنیتی پروژه VetLMS")
        print("="*60 + "\n")
        
        self.check_debug_mode()
        self.check_hardcoded_secrets()
        self.check_sql_injection_patterns()
        self.check_xss_protection()
        self.check_env_file()
        self.check_allowed_hosts()
        self.check_csrf_settings()
        
        print("\n" + "="*60)
        print("📊 نتایج بررسی")
        print("="*60 + "\n")
        
        if self.issues:
            print("🔴 مشکلات امنیتی (باید حل شوند):")
            for issue in self.issues:
                print(f"  {issue}")
            print()
        
        if self.warnings:
            print("⚠️ هشدارها (توصیه به بررسی):")
            for warning in self.warnings:
                print(f"  {warning}")
            print()
        
        if not self.issues and not self.warnings:
            print("✅ هیچ مشکل امنیتی آشکاری یافت نشد!")
        
        print("\n" + "="*60)
        print(f"کل مشکلات: {len(self.issues)}")
        print(f"کل هشدارها: {len(self.warnings)}")
        print("="*60 + "\n")
        
        return len(self.issues) == 0


if __name__ == '__main__':
    checker = SecurityChecker()
    success = checker.run_all_checks()
    
    exit(0 if success else 1)

