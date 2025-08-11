# 🔒 راهنمای امنیتی پروژه Django

## ✅ اقدامات امنیتی انجام شده

### 1. تنظیمات امنیتی پایه
- `DEBUG = False` - جلوگیری از نمایش اطلاعات حساس
- `ALLOWED_HOSTS` محدود شده
- هدرهای امنیتی فعال شده‌اند

### 2. Middleware های امنیتی
- `SecurityMiddleware` - هدرهای امنیتی
- `CSRFMiddleware` - محافظت از CSRF
- `XFrameOptionsMiddleware` - جلوگیری از Clickjacking
- `SecurityMiddleware` سفارشی - بررسی User-Agent و IP

### 3. فایل‌های خطای سفارشی
- `404.html` - صفحه یافت نشد
- `500.html` - خطای سرور
- `403.html` - دسترسی ممنوع

### 4. تنظیمات Session و Cookie
- `SESSION_COOKIE_HTTPONLY = True`
- `SESSION_EXPIRE_AT_BROWSER_CLOSE = True`
- `CSRF_COOKIE_HTTPONLY = True`

### 5. Content Security Policy
- محدودیت منابع خارجی
- محافظت از XSS
- کنترل اسکریپت‌ها و استایل‌ها

### 6. Logging و Monitoring
- ثبت خطاها در فایل
- سطح logging مناسب
- پوشه logs ایجاد شده

## 🚨 نکات مهم امنیتی

### در Production
1. **HTTPS فعال کنید:**
   ```python
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

2. **SECRET_KEY قوی استفاده کنید:**
   ```python
   SECRET_KEY = 'your-super-secret-key-here'
   ```

3. **ALLOWED_HOSTS محدود کنید:**
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

### محافظت از فایل‌ها
- فایل‌های حساس در `.gitignore` قرار دارند
- دیتابیس در repository قرار نمی‌گیرد
- فایل‌های log محافظت می‌شوند

## 🛠️ ابزارهای امنیتی

### اسکریپت بررسی امنیت
```bash
python security_check.py
```

### نصب پکیج‌های امنیتی
```bash
pip install -r requirements.txt
```

## 📋 چک‌لیست امنیتی

- [x] DEBUG = False
- [x] ALLOWED_HOSTS محدود
- [x] Middleware های امنیتی فعال
- [x] فایل‌های خطای سفارشی
- [x] تنظیمات Session امن
- [x] CSRF محافظت شده
- [x] هدرهای امنیتی
- [x] Logging فعال
- [x] .gitignore مناسب
- [ ] HTTPS فعال (در production)
- [ ] SECRET_KEY قوی
- [ ] Rate Limiting
- [ ] Two-Factor Authentication

## 🔍 بررسی‌های منظم

### روزانه
- بررسی فایل‌های log
- بررسی دسترسی‌های غیرمجاز

### هفتگی
- اجرای `security_check.py`
- بررسی به‌روزرسانی‌های Django
- بررسی پکیج‌های نصب شده

### ماهانه
- بررسی تنظیمات امنیتی
- تست نفوذ پایه
- به‌روزرسانی dependencies

## 📞 گزارش مشکلات امنیتی

در صورت مشاهده مشکل امنیتی:
1. فوراً آن را گزارش دهید
2. جزئیات کامل ارائه دهید
3. از انتشار عمومی خودداری کنید

## 📚 منابع بیشتر

- [Django Security Documentation](https://docs.djangoproject.com/en/5.2/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/) 