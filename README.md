# 🏥 سیستم مدیریت یادگیری دامپزشکی (VetLMS)

یک سیستم یادگیری و مدیریت کیس‌های پاتولوژی دامپزشکی با قابلیت‌های پیشرفته

## 📋 فهرست مطالب

- [ویژگی‌ها](#ویژگی‌ها)
- [پیش‌نیازها](#پیش‌نیازها)
- [نصب و راه‌اندازی](#نصب-و-راه‌اندازی)
- [ساختار پروژه](#ساختار-پروژه)
- [تنظیمات](#تنظیمات)
- [مستندات](#مستندات)
- [دستورات مفید](#دستورات-مفید)

## ✨ ویژگی‌ها

### 🎓 آموزش و یادگیری
- مدیریت کیس‌های پاتولوژی
- سیستم اسلاید و تصاویر
- پیگیری پیشرفت کاربران
- سیستم امتیازدهی و نمرات
- دسته‌بندی و فیلترینگ پیشرفته

### 👥 مدیریت کاربران
- سیستم احراز هویت کامل
- نقش‌های کاربری (Admin, Student)
- پروفایل کاربری
- بازیابی رمز عبور با شماره تلفن
- سیستم اشتراک و subscription

### 📊 داشبورد و گزارش‌گیری
- داشبورد مدیریتی
- داشبورد دانشجو
- آمار و تحلیل پیشرفت
- سیستم Achievements
- گزارش‌های تفصیلی

### 🔔 ارتباطات
- سیستم اعلان‌ها (Notifications)
- ارسال پیام به کاربران
- اعلان‌های broadcast

### 🔒 امنیت
- Middleware های امنیتی
- محدودیت Rate Limiting
- حفاظت در برابر حملات
- تنظیمات CORS
- Session Management امن

## 🛠 پیش‌نیازها

- Python 3.12+
- PostgreSQL 13+ (یا SQLite برای Development)
- pip
- virtualenv (اختیاری)

## 🚀 نصب و راه‌اندازی

### 1. کلون کردن پروژه

```bash
git clone <repository-url>
cd vetlms
```

### 2. ایجاد محیط مجازی

```bash
# ایجاد محیط مجازی
python -m venv venv

# فعال‌سازی
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### 4. ایجاد فایل .env

```bash
# استفاده از اسکریپت خودکار
python create_env.py

# یا کپی دستی
copy ENV_TEMPLATE.txt .env  # Windows
cp ENV_TEMPLATE.txt .env    # Linux/Mac
```

### 5. تنظیم دیتابیس

```bash
# برای استفاده از SQLite محلی
# در فایل .env:
USE_SQLITE=True

# یا برای PostgreSQL، تنظیمات را در .env وارد کنید
```

### 6. Migration دیتابیس

```bash
python manage.py migrate
```

### 7. ایجاد Superuser

```bash
python manage.py createsuperuser
```

### 8. جمع‌آوری فایل‌های استاتیک

```bash
python manage.py collectstatic --noinput
```

### 9. اجرای سرور

```bash
python manage.py runserver
```

سایت در آدرس `http://127.0.0.1:8000/` در دسترس خواهد بود.

## 📁 ساختار پروژه

```
vetlms/
├── apps/                   # تمام اپلیکیشن‌های پروژه
│   ├── __init__.py
│   │
│   ├── core/              # ماژول‌های مشترک و Utilities
│   │   ├── __init__.py
│   │   └── apps.py
│   │
│   ├── users/             # مدیریت کاربران و احراز هویت
│   │   ├── models.py      # CustomUser, Subscription, Notification
│   │   ├── views.py       # Authentication, Dashboard
│   │   ├── urls.py        # URL patterns
│   │   ├── admin.py       # Admin configuration
│   │   ├── middleware.py  # Security middlewares
│   │   ├── decorators.py  # Custom decorators
│   │   ├── management/    # Management commands
│   │   │   └── commands/
│   │   │       ├── clear_cache.py
│   │   │       └── show_config.py
│   │   ├── migrations/    # Database migrations
│   │   ├── templates/
│   │   │   └── users/    # User templates
│   │   └── static/
│   │       └── users/    # User static files
│   │
│   └── courses/           # دوره‌ها و کیس‌های آموزشی
│       ├── models.py      # Case, Slide, UserProgress
│       ├── views.py       # Course views
│       ├── api_views.py   # REST API endpoints
│       ├── serializers.py # DRF serializers
│       ├── urls.py        # URL patterns
│       ├── api_urls.py    # API URLs
│       ├── admin.py       # Admin configuration
│       ├── management/    # Management commands
│       ├── migrations/    # Database migrations
│       ├── templates/
│       │   └── courses/  # Course templates
│       └── static/
│           └── courses/  # Course static files
│
├── vetlms/                # تنظیمات اصلی Django
│   ├── settings.py       # Project settings
│   ├── urls.py           # Main URL configuration
│   ├── wsgi.py           # WSGI config
│   └── asgi.py           # ASGI config
│
├── templates/            # Template های عمومی
│   ├── 403.html         # Forbidden page
│   ├── 404.html         # Not Found page
│   ├── 500.html         # Server Error page
│   └── admin/           # Custom admin templates
│
├── static/              # فایل‌های استاتیک عمومی
├── staticfiles/         # Collected static files
├── media/               # User uploaded files
├── logs/                # Log files
│
├── docs/                # Documentation
│   ├── REFACTORING_GUIDE.md
│   └── ...
│
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── runtime.txt          # Python version
├── .env                 # Environment variables (gitignore)
├── .gitignore           # Git ignore file
├── create_env.py        # Script to create .env
├── update_content_types.py  # Script to update ContentTypes
└── README.md            # This file
```

## ⚙️ تنظیمات

### فایل .env

تمام تنظیمات حساس در فایل `.env` ذخیره می‌شوند:

```bash
# تنظیمات اصلی
DEBUG=True
SECRET_KEY=your-secret-key
ALLOW_ALL_HOSTS=False

# دیتابیس
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=your-username
DB_PASSWORD=your-password
DB_HOST=your-host
DB_PORT=5432

# برای SQLite محلی
USE_SQLITE=True

# Cache و Session
CACHE_TIMEOUT=60
SESSION_COOKIE_AGE=3600
```

### دستورات مدیریتی سفارشی

```bash
# نمایش تنظیمات فعلی
python manage.py show_config

# پاکسازی کش
python manage.py clear_cache

# ایجاد داده‌های نمونه
python manage.py create_sample_data

# پاکسازی Session های قدیمی
python manage.py clearsessions
```

## 📚 مستندات

مستندات کامل در پوشه `docs/` موجود است:

- **ENV_GUIDE.md** - راهنمای استفاده از فایل .env
- **DEBUG_FALSE_SETUP.md** - راهنمای تنظیمات Production
- **CACHE_OPTIMIZATION.md** - راهنمای بهینه‌سازی کش
- **DEPLOYMENT_README.md** - راهنمای Deploy
- **SECURITY_README.md** - راهنمای امنیت

## 🔧 دستورات مفید

### Development

```bash
# اجرای سرور توسعه
python manage.py runserver

# ایجاد migration جدید
python manage.py makemigrations

# اعمال migration ها
python manage.py migrate

# ورود به shell
python manage.py shell

# بررسی مشکلات
python manage.py check
```

### Production

```bash
# جمع‌آوری فایل‌های استاتیک
python manage.py collectstatic --noinput --clear

# اجرا با Gunicorn
gunicorn vetlms.wsgi:application --bind 0.0.0.0:8000

# تست با DEBUG=False
DEBUG=False python manage.py runserver
```

### Testing

```bash
# اجرای تست‌ها
python manage.py test

# اجرای تست با coverage
coverage run --source='.' manage.py test
coverage report
```

### Database

```bash
# ایجاد backup
python manage.py dumpdata > backup.json

# بازیابی backup
python manage.py loaddata backup.json

# ورود به دیتابیس
python manage.py dbshell

# بررسی وضعیت migration ها
python manage.py showmigrations
```

## 🌐 URL های اصلی

- **صفحه اصلی:** `/`
- **پنل ادمین:** `/admin/`
- **لاگین:** `/login/`
- **ثبت‌نام:** `/register/`
- **بازیابی رمز:** `/password-reset/`
- **داشبورد:** `/dashboard/`
- **دوره‌ها:** `/courses/`
- **API:** `/api/v1/`

## 🔒 امنیت

این پروژه شامل موارد امنیتی زیر است:

- ✅ WhiteNoise برای serve کردن فایل‌های استاتیک
- ✅ CSRF Protection
- ✅ XSS Protection
- ✅ Clickjacking Protection
- ✅ Secure Session Management
- ✅ Rate Limiting
- ✅ Custom Security Middleware
- ✅ Password Hashing با Django

⚠️ **توجه:** قبل از Deploy در Production:
1. `DEBUG=False` کنید
2. `SECRET_KEY` را تغییر دهید
3. `ALLOWED_HOSTS` را تنظیم کنید
4. از HTTPS استفاده کنید
5. دیتابیس را backup بگیرید

## 🐛 عیب‌یابی

### مشکلات رایج

**1. CSS لود نمی‌شود:**
```bash
python manage.py collectstatic --noinput
```

**2. خطای Database:**
```bash
python manage.py migrate
python manage.py check --database default
```

**3. خطای Permission:**
```bash
# Windows
icacls media /grant Users:F /T
icacls logs /grant Users:F /T
```

**4. Port در حال استفاده است:**
```bash
# استفاده از port دیگر
python manage.py runserver 8080
```

## 📝 Changelog

### نسخه 1.0.0 (اکتبر 2025)
- ✅ سیستم مدیریت کیس‌های پاتولوژی
- ✅ احراز هویت و بازیابی رمز عبور
- ✅ داشبورد مدیریتی و دانشجو
- ✅ سیستم اعلان‌ها و Subscription
- ✅ API RESTful
- ✅ پیاده‌سازی امنیتی
- ✅ بهینه‌سازی Cache
- ✅ پشتیبانی از DEBUG=False

## 🤝 مشارکت

برای مشارکت در این پروژه:

1. Fork کنید
2. Branch جدید ایجاد کنید (`git checkout -b feature/AmazingFeature`)
3. تغییرات را Commit کنید (`git commit -m 'Add some AmazingFeature'`)
4. به Branch خود Push کنید (`git push origin feature/AmazingFeature`)
5. Pull Request ایجاد کنید

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

## 👥 نویسندگان

- **HeyVoonak Team** - *کار اولیه*

## 🙏 تشکر

- Django Framework
- Django REST Framework
- WhiteNoise
- PostgreSQL/Supabase
- همه توسعه‌دهندگان متن‌باز

---

**ساخته شده با ❤️ برای آموزش دامپزشکی**
