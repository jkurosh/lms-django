# 🔧 راهنمای تنظیم DEBUG=False

## مشکل
وقتی `DEBUG=False` می‌شود، Django به طور پیش‌فرض فایل‌های استاتیک (CSS, JS, Images) را serve نمی‌کند و صفحات بدون استایل نمایش داده می‌شوند.

## راه‌حل ✅

### 1. تنظیمات انجام شده

#### الف) اضافه شدن WhiteNoise Middleware
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ اضافه شد
    # ... بقیه middleware ها
]
```

#### ب) تنظیمات Static Files
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### ج) تنظیمات URLs
```python
# Serve media files in both DEBUG=True and DEBUG=False
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
```

### 2. دستورات لازم قبل از DEBUG=False

#### مرحله 1: جمع‌آوری فایل‌های استاتیک
```bash
python manage.py collectstatic --noinput
```

این دستور تمام فایل‌های استاتیک را از `static/` به `staticfiles/` کپی می‌کند.

#### مرحله 2: بررسی فایل‌های جمع‌آوری شده
```bash
# Windows
dir staticfiles

# Linux/Mac
ls -la staticfiles/
```

باید پوشه‌های زیر را ببینید:
- `admin/` - فایل‌های ادمین Django
- `cases/` - فایل‌های استاتیک cases
- `dadash/` - فایل‌های استاتیک dadash_app
- `rest_framework/` - فایل‌های REST Framework
- و غیره...

#### مرحله 3: تست با DEBUG=False

**روش 1: تغییر موقت در settings.py**
```python
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

**روش 2: استفاده از متغیر محیطی (توصیه می‌شود)**
```bash
# Windows PowerShell
$env:DEBUG="False"
python manage.py runserver

# Windows CMD
set DEBUG=False
python manage.py runserver

# Linux/Mac
DEBUG=False python manage.py runserver
```

**روش 3: ایجاد فایل .env**
```bash
# در فایل .env
DEBUG=False
ALLOW_ALL_HOSTS=True
```

### 3. بررسی و عیب‌یابی

#### چک کردن فایل‌های استاتیک
```bash
python manage.py findstatic admin/css/base.css
python manage.py findstatic dadash/styles.css
```

#### تست در مرورگر
1. باز کردن `http://127.0.0.1:8000/`
2. فشردن `F12` برای باز کردن DevTools
3. رفتن به تب `Network`
4. رفرش صفحه (`F5`)
5. بررسی فایل‌های CSS و JS:
   - باید Status Code `200` داشته باشند
   - نه `404` یا `500`

#### بررسی Console
در تب `Console` نباید خطای زیر را ببینید:
```
Failed to load resource: the server responded with a status of 404
```

### 4. مشکلات رایج و راه‌حل

#### مشکل 1: CSS لود نمی‌شود
**علت:** فایل‌های استاتیک جمع‌آوری نشده‌اند
**راه‌حل:**
```bash
python manage.py collectstatic --clear --noinput
```

#### مشکل 2: خطای 500 Internal Server Error
**علت:** ALLOWED_HOSTS تنظیم نشده
**راه‌حل:**
```python
# در settings.py
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '::1']
```

#### مشکل 3: خطای ManifestStaticFilesStorage
**علت:** فایلی در template استفاده شده که در staticfiles نیست
**راه‌حل:**
```python
# استفاده از CompressedStaticFilesStorage بجای Manifest
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
```

#### مشکل 4: تصاویر Media لود نمی‌شوند
**راه‌حل:** قبلاً در `urls.py` تنظیم شده است ✅

### 5. دستورات مفید

#### پاکسازی و جمع‌آوری مجدد
```bash
# پاکسازی کامل
python manage.py collectstatic --clear --noinput

# جمع‌آوری مجدد
python manage.py collectstatic --noinput
```

#### بررسی تنظیمات Django
```bash
python manage.py diffsettings
```

#### تست سرور با Gunicorn (شبیه‌سازی Production)
```bash
gunicorn vetlms.wsgi:application --bind 127.0.0.1:8000
```

### 6. تنظیمات Production واقعی

#### الف) استفاده از Nginx (توصیه می‌شود)
```nginx
server {
    listen 80;
    server_name example.com;

    location /static/ {
        alias /path/to/staticfiles/;
        expires 30d;
    }

    location /media/ {
        alias /path/to/media/;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

#### ب) استفاده از Gunicorn
```bash
gunicorn vetlms.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 60
```

#### ج) متغیرهای محیطی Production
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://...
```

### 7. چک‌لیست قبل از Production

- [ ] `python manage.py collectstatic` اجرا شده
- [ ] `DEBUG=False` تنظیم شده
- [ ] `SECRET_KEY` تصادفی و امن است
- [ ] `ALLOWED_HOSTS` شامل دامنه اصلی است
- [ ] فایل‌های استاتیک به درستی لود می‌شوند
- [ ] تمام صفحات بدون خطا باز می‌شوند
- [ ] لاگ‌ها بررسی شده‌اند
- [ ] دیتابیس backup گرفته شده
- [ ] SSL/HTTPS فعال است (در production)

### 8. تست نهایی

```bash
# 1. جمع‌آوری فایل‌های استاتیک
python manage.py collectstatic --noinput

# 2. تست با DEBUG=False
DEBUG=False python manage.py runserver

# 3. باز کردن مرورگر
# http://127.0.0.1:8000/

# 4. بررسی صفحات
# ✅ صفحه اصلی
# ✅ صفحه لاگین
# ✅ صفحه ثبت‌نام
# ✅ صفحه ادمین
```

### 9. یادآوری مهم ⚠️

#### در Development:
```python
DEBUG = True
ALLOWED_HOSTS = ['*']
```

#### در Production:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = 'your-very-secure-random-key'
```

### 10. دریافت کمک

اگر مشکلی وجود دارد:

1. **بررسی لاگ‌ها:**
```bash
# در terminal که سرور اجرا می‌کنید
```

2. **بررسی Console مرورگر:**
   - F12 → Console
   - F12 → Network

3. **تست با DEBUG=True:**
```bash
DEBUG=True python manage.py runserver
```

4. **بررسی فایل staticfiles:**
```bash
ls -la staticfiles/
```

## نتیجه 🎉

با این تنظیمات، سایت شما در هر دو حالت `DEBUG=True` و `DEBUG=False` به درستی کار می‌کند:

✅ CSS/JS به درستی لود می‌شوند
✅ تصاویر و فایل‌های media نمایش داده می‌شوند  
✅ WhiteNoise فایل‌های استاتیک را serve می‌کند
✅ آماده برای Production است

---
**تاریخ:** اکتبر 2025  
**نسخه:** 1.0

