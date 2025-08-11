# راهنمای Deploy پروژه VetLMS روی Vercel

## مرحله 1: آماده‌سازی پروژه

پروژه شما آماده deployment است. فایل‌های زیر ایجاد شده‌اند:

- `vercel.json` - تنظیمات Vercel
- `requirements.txt` - پکیج‌های مورد نیاز
- `runtime.txt` - نسخه Python
- `build_files.sh` - اسکریپت build

## مرحله 2: Deploy روی Vercel

### روش 1: از طریق Vercel CLI

1. نصب Vercel CLI:
```bash
npm i -g vercel
```

2. Login به Vercel:
```bash
vercel login
```

3. Deploy پروژه:
```bash
vercel
```

### روش 2: از طریق GitHub

1. پروژه را به GitHub push کنید
2. در [vercel.com](https://vercel.com) ثبت‌نام کنید
3. "New Project" را کلیک کنید
4. GitHub repository را انتخاب کنید
5. تنظیمات را تایید کنید و Deploy کنید

## مرحله 3: تنظیمات محیطی

در Vercel dashboard، متغیرهای محیطی زیر را تنظیم کنید:

```
DJANGO_SETTINGS_MODULE=vetlms.settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-vercel-domain.vercel.app
```

## مرحله 4: Database

برای production، از PostgreSQL استفاده کنید:

1. در Vercel، "Storage" را اضافه کنید
2. PostgreSQL database ایجاد کنید
3. متغیر `DATABASE_URL` را تنظیم کنید

## نکات مهم

- پروژه شما حالا هیچ تست پیش‌فرضی نمایش نمی‌دهد
- تمام داده‌ها باید از پنل ادمین وارد شوند
- فایل‌های media در Vercel ذخیره نمی‌شوند (از cloud storage استفاده کنید)
- برای production، `DEBUG=False` تنظیم کنید

## تست محلی

قبل از deploy، تست کنید:

```bash
python manage.py collectstatic
python manage.py migrate
python manage.py runserver
```
