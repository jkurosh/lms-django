#!/usr/bin/env python
"""
اسکریپت تست امنیتی برای بررسی آسیب‌پذیری‌های احتمالی
"""
import os
import sys
import django
import requests
from urllib.parse import urljoin

# تنظیم Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetlms.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.db import connection
from django.conf import settings
import json

User = get_user_model()

class SecurityTester:
    def __init__(self, base_url='http://127.0.0.1:8000'):
        self.base_url = base_url
        self.client = Client()
        self.vulnerabilities = []
        self.passed_tests = []
        
    def log_vulnerability(self, test_name, severity, description, recommendation):
        """ثبت آسیب‌پذیری"""
        self.vulnerabilities.append({
            'test': test_name,
            'severity': severity,
            'description': description,
            'recommendation': recommendation
        })
        print(f"[FAIL] [{severity}] {test_name}: {description}")
        print(f"   [TIP] توصيه: {recommendation}\n")
    
    def log_pass(self, test_name):
        """ثبت تست موفق"""
        self.passed_tests.append(test_name)
        print(f"[PASS] {test_name}: OK\n")
    
    def test_sql_injection_login(self):
        """تست SQL Injection در لاگین"""
        print("[TEST] تست SQL Injection در لاگين...")
        
        sql_payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' /*",
            "admin'--",
            "admin'/*",
            "' UNION SELECT NULL--",
            "1' OR '1'='1",
        ]
        
        for payload in sql_payloads:
            try:
                response = self.client.post('/login/', {
                    'username': payload,
                    'password': payload
                }, follow=True)
                
                # بررسی خطاهای SQL در پاسخ
                if 'sql' in response.content.decode('utf-8', errors='ignore').lower():
                    self.log_vulnerability(
                        'SQL Injection در لاگین',
                        'CRITICAL',
                        f'پاسخ حاوی خطای SQL است با payload: {payload}',
                        'از Django ORM استفاده کنید و هرگز از raw SQL با user input استفاده نکنید'
                    )
                    return
                    
            except Exception as e:
                if 'sql' in str(e).lower() or 'syntax' in str(e).lower():
                    self.log_vulnerability(
                        'SQL Injection در لاگین',
                        'CRITICAL',
                        f'خطای SQL با payload: {payload}',
                        'از Django ORM استفاده کنید'
                    )
                    return
        
        self.log_pass('SQL Injection در لاگین')
    
    def test_xss_vulnerability(self):
        """تست XSS در فیلدهای ورودی"""
        print("[TEST] تست XSS (Cross-Site Scripting)...")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src=javascript:alert('XSS')>",
            "<body onload=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
        ]
        
        # تست در فرم ثبت‌نام
        for payload in xss_payloads:
            try:
                response = self.client.post('/register/', {
                    'username': payload,
                    'first_name': payload,
                    'last_name': payload,
                    'phone_number': '09123456789',
                    'password1': 'Test1234!',
                    'password2': 'Test1234!',
                }, follow=True)
                
                content = response.content.decode('utf-8', errors='ignore')
                
                # بررسی اینکه آیا payload در خروجی HTML رندر شده است
                if payload in content and '<script>' in payload:
                    # بررسی اینکه آیا escape شده است
                    if payload.replace('<', '&lt;') not in content:
                        self.log_vulnerability(
                            'XSS در فرم ثبت‌نام',
                            'HIGH',
                            f'Payload XSS در خروجی HTML رندر شده: {payload[:30]}...',
                            'از Django template filters مثل |escape یا |safe استفاده کنید'
                        )
                        return
                        
            except Exception as e:
                pass
        
        self.log_pass('XSS در فرم‌ها')
    
    def test_csrf_protection(self):
        """تست محافظت CSRF"""
        print("[TEST] تست محافظت CSRF...")
        
        try:
            # تلاش برای ارسال POST بدون CSRF token
            response = self.client.post('/login/', {
                'username': 'test',
                'password': 'test'
            }, follow=True)
            
            # اگر بدون CSRF token پذیرفته شد، آسیب‌پذیری وجود دارد
            if response.status_code == 200 and 'csrf' not in response.content.decode('utf-8', errors='ignore').lower():
                # بررسی اینکه آیا middleware CSRF فعال است
                if 'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE:
                    # اگر middleware فعال است اما خطا نمی‌دهد، مشکل دارد
                    if 'Forbidden' not in str(response.content):
                        self.log_vulnerability(
                            'محافظت CSRF',
                            'HIGH',
                            'فرم بدون CSRF token پذیرفته شد',
                            'مطمئن شوید که CsrfViewMiddleware فعال است و {% csrf_token %} در فرم‌ها وجود دارد'
                        )
                        return
        
        except Exception as e:
            if 'csrf' in str(e).lower() or 'forbidden' in str(e).lower():
                self.log_pass('محافظت CSRF')
                return
        
        self.log_pass('محافظت CSRF')
    
    def test_authentication_bypass(self):
        """تست دور زدن احراز هویت"""
        print("[TEST] تست دور زدن احراز هويت...")
        
        # تست دسترسی به صفحات محافظت شده بدون لاگین
        protected_urls = [
            '/dashboard/',
            '/admin/',
            '/my-cases/',
            '/profile/',
        ]
        
        for url in protected_urls:
            try:
                response = self.client.get(url, follow=True)
                
                # اگر به صفحه لاگین redirect نشد، آسیب‌پذیری وجود دارد
                if '/login/' not in response.redirect_chain and response.status_code == 200:
                    # بررسی محتوای صفحه
                    content = response.content.decode('utf-8', errors='ignore')
                    if 'dashboard' in content.lower() or 'پروفایل' in content:
                        self.log_vulnerability(
                            'دور زدن احراز هویت',
                            'CRITICAL',
                            f'دسترسی به {url} بدون احراز هویت',
                            'از @login_required decorator استفاده کنید'
                        )
                        return
                        
            except Exception as e:
                pass
        
        self.log_pass('محافظت احراز هویت')
    
    def test_rate_limiting(self):
        """تست Rate Limiting"""
        print("[TEST] تست Rate Limiting...")
        
        # ارسال درخواست‌های زیاد به endpoint لاگین
        max_requests = 20
        success_count = 0
        
        for i in range(max_requests):
            try:
                response = self.client.post('/login/', {
                    'username': 'test',
                    'password': 'wrong_password'
                }, follow=True)
                
                if response.status_code == 200:
                    success_count += 1
                    
            except Exception as e:
                pass
        
        # اگر همه درخواست‌ها پذیرفته شدند، rate limiting کار نمی‌کند
        if success_count == max_requests:
            self.log_vulnerability(
                'Rate Limiting',
                'MEDIUM',
                f'Rate limiting کار نمی‌کند - {max_requests} درخواست پذیرفته شد',
                'از decorator @rate_limit استفاده کنید یا middleware rate limiting اضافه کنید'
            )
        else:
            self.log_pass('Rate Limiting')
    
    def test_input_validation(self):
        """تست اعتبارسنجی ورودی"""
        print("[TEST] تست اعتبارسنجي ورودي...")
        
        # تست ورودی‌های نامعتبر
        invalid_inputs = [
            {'username': '', 'password': 'test'},  # خالی
            {'username': 'a' * 1000, 'password': 'test'},  # خیلی طولانی
            {'username': 'test<script>', 'password': 'test'},  # کاراکترهای خاص
            {'phone_number': '123'},  # شماره تلفن نامعتبر
        ]
        
        for invalid_input in invalid_inputs:
            try:
                if 'username' in invalid_input:
                    response = self.client.post('/register/', invalid_input, follow=True)
                    
                    # بررسی اینکه آیا اعتبارسنجی انجام شده است
                    content = response.content.decode('utf-8', errors='ignore')
                    if 'error' not in content.lower() and 'invalid' not in content.lower():
                        if invalid_input['username'] == '':
                            self.log_vulnerability(
                                'اعتبارسنجی ورودی',
                                'MEDIUM',
                                'فیلدهای خالی پذیرفته می‌شوند',
                                'از Django forms و validators استفاده کنید'
                            )
                            return
                            
            except Exception as e:
                pass
        
        self.log_pass('اعتبارسنجی ورودی')
    
    def test_sql_injection_in_queries(self):
        """تست SQL Injection در کوئری‌های Django"""
        print("[TEST] تست SQL Injection در كويري‌هاي Django...")
        
        # بررسی استفاده از raw SQL
        from django.apps import apps
        
        vulnerable_patterns = [
            'raw(',
            'execute(',
            'cursor.execute',
            'extra(',
        ]
        
        # بررسی فایل‌های views
        import os
        views_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apps', 'users', 'views.py')
        
        if os.path.exists(views_file):
            with open(views_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                for pattern in vulnerable_patterns:
                    if pattern in content:
                        # بررسی اینکه آیا user input در raw SQL استفاده شده است
                        if 'request.POST' in content or 'request.GET' in content:
                            self.log_vulnerability(
                                'SQL Injection در Raw Queries',
                                'CRITICAL',
                                f'استفاده از {pattern} در views.py',
                                'از Django ORM استفاده کنید. اگر مجبور به raw SQL هستید، از parameterized queries استفاده کنید'
                            )
                            return
        
        self.log_pass('SQL Injection در کوئری‌ها')
    
    def test_debug_mode(self):
        """بررسی حالت DEBUG"""
        print("[TEST] بررسي حالت DEBUG...")
        
        if settings.DEBUG:
            self.log_vulnerability(
                'DEBUG Mode',
                'HIGH',
                'DEBUG=True در production فعال است',
                'DEBUG را در production روی False قرار دهید'
            )
        else:
            self.log_pass('DEBUG Mode')
    
    def test_secret_key(self):
        """بررسی SECRET_KEY"""
        print("[TEST] بررسي SECRET_KEY...")
        
        secret_key = settings.SECRET_KEY
        
        if 'insecure' in secret_key.lower() or secret_key == 'django-insecure-REPLACED-FOR-SECURITY':
            self.log_vulnerability(
                'SECRET_KEY',
                'CRITICAL',
                'SECRET_KEY پیش‌فرض یا ناامن استفاده شده است',
                'یک SECRET_KEY قوی و منحصر به فرد تولید کنید و در environment variables قرار دهید'
            )
        else:
            self.log_pass('SECRET_KEY')
    
    def test_password_storage(self):
        """بررسی ذخیره‌سازی رمز عبور"""
        print("[TEST] بررسي ذخيره‌سازي رمز عبور...")
        
        # Django به صورت پیش‌فرض از PBKDF2 استفاده می‌کند که امن است
        # اما بررسی می‌کنیم که آیا password به صورت plain text ذخیره نشده است
        
        try:
            # ایجاد یک کاربر تست
            test_user = User.objects.filter(username='security_test_user').first()
            if not test_user:
                test_user = User.objects.create_user(
                    username='security_test_user',
                    password='TestPassword123!',
                    email='test@test.com'
                )
            
            # بررسی password hash
            if test_user.password.startswith('pbkdf2_') or test_user.password.startswith('bcrypt'):
                self.log_pass('ذخیره‌سازی رمز عبور')
            else:
                self.log_vulnerability(
                    'ذخیره‌سازی رمز عبور',
                    'CRITICAL',
                    'رمز عبور به صورت hash ذخیره نشده است',
                    'از Django authentication system استفاده کنید که به صورت پیش‌فرض رمزها را hash می‌کند'
                )
            
            # حذف کاربر تست
            test_user.delete()
            
        except Exception as e:
            self.log_vulnerability(
                'ذخیره‌سازی رمز عبور',
                'MEDIUM',
                f'خطا در بررسی: {str(e)}',
                'بررسی کنید که Django authentication system به درستی کار می‌کند'
            )
    
    def generate_report(self):
        """تولید گزارش نهایی"""
        print("\n" + "="*60)
        print("[REPORT] گزارش نهايي تست امنيتي")
        print("="*60)
        
        total_tests = len(self.passed_tests) + len(self.vulnerabilities)
        passed = len(self.passed_tests)
        failed = len(self.vulnerabilities)
        
        print(f"\n[PASS] تست‌هاي موفق: {passed}/{total_tests}")
        print(f"[FAIL] آسيب‌پذيري‌ها: {failed}/{total_tests}")
        
        if self.vulnerabilities:
            print("\n[VULN] آسيب‌پذيري‌هاي يافت شده:")
            print("-" * 60)
            
            # دسته‌بندی بر اساس severity
            critical = [v for v in self.vulnerabilities if v['severity'] == 'CRITICAL']
            high = [v for v in self.vulnerabilities if v['severity'] == 'HIGH']
            medium = [v for v in self.vulnerabilities if v['severity'] == 'MEDIUM']
            
            if critical:
                print("\n[CRITICAL] CRITICAL:")
                for v in critical:
                    print(f"   - {v['test']}: {v['description']}")
            
            if high:
                print("\n[HIGH] HIGH:")
                for v in high:
                    print(f"   - {v['test']}: {v['description']}")
            
            if medium:
                print("\n[MEDIUM] MEDIUM:")
                for v in medium:
                    print(f"   - {v['test']}: {v['description']}")
        else:
            print("\n[OK] هيچ آسيب‌پذيري يافت نشد!")
        
        print("\n" + "="*60)
        
        return {
            'total': total_tests,
            'passed': passed,
            'failed': failed,
            'vulnerabilities': self.vulnerabilities
        }

def main():
    import sys
    import io
    # Fix encoding for Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    print("[SECURITY] شروع تست امنيتي...\n")
    
    tester = SecurityTester()
    
    # اجرای تست‌ها
    tester.test_debug_mode()
    tester.test_secret_key()
    tester.test_sql_injection_login()
    tester.test_sql_injection_in_queries()
    tester.test_xss_vulnerability()
    tester.test_csrf_protection()
    tester.test_authentication_bypass()
    tester.test_rate_limiting()
    tester.test_input_validation()
    tester.test_password_storage()
    
    # تولید گزارش
    report = tester.generate_report()
    
    # ذخیره گزارش در فایل
    report_file = os.path.join(os.path.dirname(__file__), 'security_report.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[FILE] گزارش كامل در {report_file} ذخيره شد.")
    
    return 0 if report['failed'] == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
