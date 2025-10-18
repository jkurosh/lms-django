# 📦 راهنمای کامل استفاده از فایل .env

## 🎯 هدف

فایل `.env` برای ذخیره تنظیمات محیطی (Environment Variables) استفاده می‌شود که نباید در Git commit شوند، مانند:
- رمزهای عبور دیتابیس
- کلیدهای مخفی (SECRET_KEY)
- تنظیمات محیط‌های مختلف (Development/Production)

## 🚀 نحوه ایجاد فایل .env

### روش 1: استفاده از اسکریپت خودکار (توصیه می‌شود) ✅

```bash
python create_env.py
```

### روش 2: کپی دستی

**Windows PowerShell:**
```powershell
Copy-Item ENV_TEMPLATE.txt .env
```

**Windows CMD:**
```cmd
copy ENV_TEMPLATE.txt .env
```

**Linux/Mac:**
```bash
cp ENV_TEMPLATE.txt .env
```

### روش 3: ایجاد دستی

فایل جدیدی با نام `.env` در ریشه پروژه ایجاد کنید و محتوای `ENV_TEMPLATE.txt` را در آن کپی کنید.

## 📝 تنظیمات مهم

### 1. تنظیمات اصلی

```bash
# حالت Debug
DEBUG=True              # True برای توسعه
                       # False برای production

# کلید مخفی
SECRET_KEY=your-secret-key-here

# دسترسی Host ها
ALLOW_ALL_HOSTS=False   # True فقط برای تست محلی
```

### 2. تنظیمات دیتابیس

#### PostgreSQL (Supabase):
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=your-username
DB_PASSWORD=your-password
DB_HOST=your-host.supabase.com
DB_PORT=6543
USE_SQLITE=False
```

#### SQLite (توسعه محلی):
```bash
USE_SQLITE=True
```

#### MySQL:
```bash
DB_ENGINE=django.db.backends.mysql
DB_NAME=vetlms
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

### 3. تنظیمات Cache و Session

```bash
# زمان کش (ثانیه)
CACHE_TIMEOUT=60        # 0 برای غیرفعال کردن
                        # 300 برای 5 دقیقه (production)

# عمر Session
SESSION_COOKIE_AGE=3600 # 1 ساعت
                        # 86400 برای 24 ساعت
```

### 4. تنظیمات Email (اختیاری)

```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

💡 **نکته:** برای Gmail باید از [App Password](https://myaccount.google.com/apppasswords) استفاده کنید.

## 🎨 پروفایل‌های محیط مختلف

### 🏠 Development (توسعه محلی)

```bash
# .env
DEBUG=True
USE_SQLITE=True
ALLOW_ALL_HOSTS=True
CACHE_TIMEOUT=0
LOG_LEVEL=DEBUG
```

### 🧪 Testing (تست)

```bash
# .env.test
DEBUG=True
USE_SQLITE=True
ALLOW_ALL_HOSTS=False
CACHE_TIMEOUT=0
LOG_LEVEL=INFO
```

### 🚀 Production (تولید)

```bash
# .env.production
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
SECURE_SSL_REDIRECT=True
CACHE_TIMEOUT=300
ALLOW_ALL_HOSTS=False
LOG_LEVEL=WARNING

# تنظیمات امنیتی
SECURE_HSTS_SECONDS=31536000
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

## 🔐 امنیت

### ایجاد SECRET_KEY جدید

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### چک‌لیست امنیتی

- [ ] SECRET_KEY منحصر به فرد و تصادفی است
- [ ] فایل .env در .gitignore است
- [ ] DEBUG=False در production
- [ ] رمزهای قوی برای دیتابیس
- [ ] ALLOWED_HOSTS محدود به دامنه‌های مشخص
- [ ] SECURE_SSL_REDIRECT=True در production
- [ ] از HTTPS استفاده می‌شود

## 📋 دستورات مفید

### بررسی بارگذاری متغیرها

```python
# در Python shell
python manage.py shell

>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>> print(os.getenv('DEBUG'))
True
```

### تست با تنظیمات مختلف

```bash
# تست با DEBUG=False
DEBUG=False python manage.py runserver

# تست با SQLite
USE_SQLITE=True python manage.py runserver

# تست با کش غیرفعال
CACHE_TIMEOUT=0 python manage.py runserver
```

## 🔄 تغییر بین محیط‌ها

### استفاده از فایل‌های .env مختلف

```bash
# Development
python manage.py runserver

# Production
python manage.py runserver --settings=vetlms.settings_production
```

### یا استفاده از متغیر محیطی

```bash
# Windows PowerShell
$env:DJANGO_SETTINGS_MODULE="vetlms.settings_production"

# Linux/Mac
export DJANGO_SETTINGS_MODULE=vetlms.settings_production
```

## ⚠️ مشکلات رایج

### 1. متغیرها بارگذاری نمی‌شوند

**علت:** فایل .env در مسیر صحیح نیست یا python-dotenv نصب نیست

**راه‌حل:**
```bash
pip install python-dotenv
```

### 2. تغییرات اعمال نمی‌شوند

**علت:** سرور را restart نکرده‌اید

**راه‌حل:**
```bash
# سرور را متوقف کنید (Ctrl+C)
# دوباره اجرا کنید
python manage.py runserver
```

### 3. خطای DEBUG=False

**علت:** ALLOWED_HOSTS تنظیم نشده

**راه‌حل:**
```bash
ALLOW_ALL_HOSTS=True  # فقط برای تست
```

### 4. دیتابیس متصل نمی‌شود

**راه‌حل:**
```bash
# بررسی تنظیمات دیتابیس
python manage.py check --database default

# تست اتصال
python manage.py dbshell
```

## 📁 ساختار فایل‌های .env

```
vetlms/
├── .env                 # محیط اصلی (gitignore شده)
├── .env.example         # نمونه (در git)
├── .env.local          # محلی (gitignore شده)
├── .env.production     # تولید (gitignore شده)
├── .env.test           # تست (gitignore شده)
├── ENV_TEMPLATE.txt    # قالب (در git)
└── create_env.py       # اسکریپت ایجاد (در git)
```

## 🎓 مثال‌های کاربردی

### مثال 1: تست سریع با SQLite

```bash
# ایجاد فایل .env
echo "DEBUG=True" > .env
echo "USE_SQLITE=True" >> .env
echo "ALLOW_ALL_HOSTS=True" >> .env

# اجرای سرور
python manage.py migrate
python manage.py runserver
```

### مثال 2: آماده‌سازی برای Production

```bash
# تولید SECRET_KEY جدید
NEW_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

# ایجاد .env.production
cat > .env.production << EOF
DEBUG=False
SECRET_KEY=$NEW_KEY
DB_ENGINE=django.db.backends.postgresql
SECURE_SSL_REDIRECT=True
CACHE_TIMEOUT=300
ALLOW_ALL_HOSTS=False
EOF
```

### مثال 3: Deployment به Vercel

```bash
# تنظیمات Vercel
echo "VERCEL=True" >> .env
echo "VERCEL_DOMAIN=yourapp.vercel.app" >> .env

# در Vercel Dashboard:
# Settings > Environment Variables
# اضافه کردن تمام متغیرها
```

## 📚 منابع بیشتر

- [Django Settings Best Practices](https://docs.djangoproject.com/en/stable/topics/settings/)
- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [12 Factor App](https://12factor.net/config)
- [Security Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

## ✅ چک‌لیست نهایی

قبل از Deploy:

- [ ] فایل .env ایجاد شده
- [ ] SECRET_KEY منحصر به فرد است
- [ ] DEBUG=False برای production
- [ ] دیتابیس تنظیم شده
- [ ] ALLOWED_HOSTS محدود شده
- [ ] تنظیمات امنیتی فعال است
- [ ] Email تنظیم شده (اختیاری)
- [ ] Cache تنظیم شده
- [ ] لاگ‌ها بررسی شده‌اند
- [ ] فایل .env در git نیست

---
**تاریخ:** اکتبر 2025  
**نسخه:** 1.0  
**نویسنده:** HeyVoonak Team

