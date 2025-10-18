# 🚀 راهنمای کامل Deploy پروژه VetLMS روی Vercel

## 📋 پیش‌نیازها

### 1. حساب Vercel
- ثبت‌نام در [vercel.com](https://vercel.com)
- اتصال حساب GitHub

### 2. دیتابیس Cloud
- **Supabase** (توصیه شده) - رایگان تا 500MB
- **PlanetScale** - رایگان تا 1GB  
- **Railway** - رایگان تا 500MB
- **Clever Cloud** - رایگان تا 1GB

### 3. Git Repository
- پروژه باید در GitHub باشد
- تمام فایل‌ها commit شده باشند

---

## 🎯 مرحله 1: آماده‌سازی پروژه

### فایل‌های ایجاد شده:

✅ **فایل‌های اصلی:**
- `api/index.py` - ورودی اصلی WSGI
- `api/requirements.txt` - پکیج‌های Python
- `api/vercel.json` - تنظیمات Vercel
- `vercel.json` - تنظیمات کلی پروژه
- `runtime.txt` - نسخه Python

✅ **فایل‌های Build:**
- `build.sh` - اسکریپت build برای Linux
- `build.bat` - اسکریپت build برای Windows

✅ **تنظیمات بهینه شده:**
- `vetlms/settings.py` - بهینه‌سازی برای Vercel

---

## 🗄️ مرحله 2: راه‌اندازی دیتابیس

### گزینه A: Supabase (توصیه شده)

1. **ایجاد پروژه:**
   - به [supabase.com](https://supabase.com) بروید
   - "New Project" کلیک کنید
   - نام پروژه: `vetlms`
   - رمز عبور قوی انتخاب کنید

2. **کپی اطلاعات اتصال:**
   - به "Settings" > "Database" بروید
   - "Connection string" را کپی کنید
   - فرمت: `postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres`

### گزینه B: PlanetScale

1. **ایجاد دیتابیس:**
   - به [planetscale.com](https://planetscale.com) بروید
   - "Create database" کلیک کنید
   - نام: `vetlms`

2. **کپی اطلاعات اتصال:**
   - "Connect" کلیک کنید
   - "General" > "Connection string" را کپی کنید

---

## 🚀 مرحله 3: Deploy روی Vercel

### روش 1: از طریق Vercel Dashboard (توصیه شده)

1. **وارد شدن به Vercel:**
   - به [vercel.com](https://vercel.com) بروید
   - "Login" کلیک کنید

2. **ایجاد پروژه جدید:**
   - "New Project" کلیک کنید
   - GitHub repository را انتخاب کنید
   - "Import" کلیک کنید

3. **تنظیمات پروژه:**
   ```
   Framework Preset: Other
   Root Directory: ./
   Build Command: python manage.py collectstatic --noinput
   Output Directory: staticfiles
   Install Command: pip install -r api/requirements.txt
   ```

4. **Environment Variables:**
   ```env
   # Django Settings
   DJANGO_SETTINGS_MODULE=vetlms.settings
   SECRET_KEY=your-very-secret-key-here-change-this
   DEBUG=False
   IS_VERCEL=True
   
   # Database
   DATABASE_URL=postgresql://user:pass@host:port/dbname
   
   # Security
   ALLOWED_HOSTS=your-domain.vercel.app
   
   # Payment Gateway (اختیاری)
   ZARINPAL_MERCHANT_ID=your-merchant-id
   ZARINPAL_ACCESS_TOKEN=your-access-token
   ZARINPAL_SANDBOX=True
   
   # SMS Provider (اختیاری)
   KAVENEGAR_API_KEY=your-api-key
   FARAZ_SMS_API_KEY=your-faraz-key
   ```

5. **Deploy:**
   - "Deploy" کلیک کنید
   - منتظر بمانید تا build تمام شود

### روش 2: از طریق Vercel CLI

1. **نصب Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **تنظیم Environment Variables:**
   ```bash
   vercel env add SECRET_KEY
   vercel env add DATABASE_URL
   vercel env add DEBUG
   # ... سایر متغیرها
   ```

---

## ⚙️ مرحله 4: تنظیمات پس از Deploy

### 1. اجرای Migration ها

**روش A: از طریق Vercel CLI:**
```bash
vercel env pull .env.local
python manage.py migrate
```

**روش B: از طریق Vercel Dashboard:**
- به "Functions" بروید
- "index.py" را انتخاب کنید
- در Console اجرا کنید:
```python
import os
os.system('python manage.py migrate')
```

### 2. ایجاد Superuser

**از طریق Vercel CLI:**
```bash
python manage.py createsuperuser
```

### 3. جمع‌آوری Static Files

Static files به صورت خودکار جمع‌آوری می‌شوند، اما اگر نیاز به refresh داشتید:
```bash
python manage.py collectstatic --noinput
```

---

## 🔧 مرحله 5: تنظیمات پیشرفته

### 1. Custom Domain

1. **در Vercel Dashboard:**
   - "Settings" > "Domains" بروید
   - دامنه خود را اضافه کنید
   - DNS records را تنظیم کنید

2. **به‌روزرسانی ALLOWED_HOSTS:**
   ```env
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-project.vercel.app
   ```

### 2. SSL Certificate

Vercel به صورت خودکار SSL certificate ارائه می‌دهد.

### 3. Environment Variables برای Production

```env
# Production Settings
DEBUG=False
SECRET_KEY=production-secret-key-very-long-and-secure
ALLOWED_HOSTS=yourdomain.com,your-project.vercel.app

# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Payment Gateway (Production)
ZARINPAL_SANDBOX=False
ZARINPAL_MERCHANT_ID=your-production-merchant-id

# SMS (Production)
FARAZ_SMS_API_KEY=your-production-api-key
```

---

## 🧪 مرحله 6: تست و بررسی

### 1. تست عملکرد سایت

```bash
# تست محلی
vercel dev

# بازدید از:
# http://localhost:3000
```

### 2. تست API Endpoints

```bash
# تست API
curl https://your-project.vercel.app/api/cases/
curl https://your-project.vercel.app/admin/
```

### 3. بررسی Log ها

**در Vercel Dashboard:**
- "Functions" > "index.py" > "View Function Logs"

**از طریق CLI:**
```bash
vercel logs your-project.vercel.app
```

---

## 🚨 عیب‌یابی مشکلات رایج

### ❌ خطای "Module not found"

**راه‌حل:**
```bash
# بررسی requirements.txt
pip install -r api/requirements.txt

# Deploy مجدد
vercel --prod
```

### ❌ خطای "Database connection failed"

**راه‌حل:**
1. بررسی `DATABASE_URL` در Environment Variables
2. بررسی اینکه دیتابیس در دسترس است
3. تست اتصال محلی:
```python
python manage.py shell
>>> from django.db import connection
>>> cursor = connection.cursor()
>>> cursor.execute("SELECT 1")
```

### ❌ خطای "Static files not found"

**راه‌حل:**
```bash
# اجرای collectstatic
python manage.py collectstatic --noinput

# بررسی STATIC_ROOT در settings.py
```

### ❌ خطای "SECRET_KEY not set"

**راه‌حل:**
```env
SECRET_KEY=django-insecure-your-secret-key-here
```

### ❌ خطای "ALLOWED_HOSTS"

**راه‌حل:**
```env
ALLOWED_HOSTS=your-domain.vercel.app,localhost,127.0.0.1
```

---

## 📊 مانیتورینگ و بهینه‌سازی

### 1. Performance Monitoring

**Vercel Analytics:**
- در Dashboard > "Analytics" فعال کنید
- عملکرد سایت را بررسی کنید

### 2. Database Monitoring

**Supabase:**
- به Dashboard بروید
- "Database" > "Logs" را بررسی کنید

### 3. Error Tracking

**Vercel Logs:**
- "Functions" > "index.py" > "Logs"
- خطاها را بررسی کنید

---

## 🔄 به‌روزرسانی پروژه

### 1. تغییرات کد

```bash
# Commit تغییرات
git add .
git commit -m "Update for production"
git push origin main

# Vercel خودکار deploy می‌کند
```

### 2. تغییرات Environment Variables

```bash
# از طریق CLI
vercel env add NEW_VARIABLE

# یا از طریق Dashboard
# Settings > Environment Variables
```

### 3. Rollback

```bash
# بازگشت به نسخه قبلی
vercel rollback [deployment-url]
```

---

## 📝 چک‌لیست نهایی

### ✅ قبل از Deploy:
- [ ] تمام فایل‌ها commit شده‌اند
- [ ] `requirements.txt` به‌روز است
- [ ] `SECRET_KEY` تنظیم شده
- [ ] دیتابیس آماده است
- [ ] Environment Variables تنظیم شده‌اند

### ✅ بعد از Deploy:
- [ ] سایت در دسترس است
- [ ] Admin panel کار می‌کند
- [ ] API endpoints پاسخ می‌دهند
- [ ] Static files لود می‌شوند
- [ ] دیتابیس متصل است
- [ ] Migration ها اجرا شده‌اند

### ✅ تست عملکرد:
- [ ] صفحه اصلی لود می‌شود
- [ ] لاگین کار می‌کند
- [ ] API calls موفق هستند
- [ ] فایل‌های media نمایش داده می‌شوند

---

## ◀️ بازگشت به Development

برای بازگشت به محیط توسعه:

```bash
# تنظیم Environment Variables محلی
DEBUG=True
IS_VERCEL=False
USE_SQLITE=true

# اجرای سرور محلی
python manage.py runserver
```

---

## 🆘 پشتیبانی

### **Vercel:**
- [Documentation](https://vercel.com/docs)
- [Support](https://vercel.com/support)
- [Community](https://github.com/vercel/vercel/discussions)

### **Django:**
- [Deployment Guide](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Static Files](https://docs.djangoproject.com/en/stable/howto/static-files/)

### **Supabase:**
- [Documentation](https://supabase.com/docs)
- [Support](https://supabase.com/support)

---

## 🎉 تبریک!

پروژه VetLMS شما حالا روی Vercel در دسترس است! 🚀

**آدرس سایت:** `https://your-project.vercel.app`

**Admin Panel:** `https://your-project.vercel.app/admin/`

**API Base:** `https://your-project.vercel.app/api/`
