# راهنمای راه‌اندازی زرین‌پال

## 📋 مراحل راه‌اندازی

### 1️⃣ دریافت Merchant ID

1. به سایت [زرین‌پال](https://www.zarinpal.com) بروید
2. ثبت‌نام کنید یا وارد شوید
3. از پنل کاربری، Merchant ID خود را کپی کنید

### 2️⃣ تنظیمات Environment Variables

فایل `.env` در ریشه پروژه بسازید:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Zarinpal Payment Gateway
ZARINPAL_MERCHANT_ID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
ZARINPAL_ACCESS_TOKEN=your-access-token-here
ZARINPAL_SANDBOX=True
ZARINPAL_CALLBACK_URL=http://127.0.0.1:8000/payment/callback/
```

### 3️⃣ حالت Sandbox (تست)

برای تست پرداخت بدون واریز واقعی پول:

```env
ZARINPAL_SANDBOX=True
```

### 4️⃣ حالت Production (محیط واقعی)

برای پرداخت واقعی:

```env
ZARINPAL_SANDBOX=False
ZARINPAL_MERCHANT_ID=YOUR-REAL-MERCHANT-ID
ZARINPAL_CALLBACK_URL=https://yourdomain.com/payment/callback/
```

## 🔗 URLهای موجود

```python
# پرداخت مستقیم یک پلن
/payment/start/<plan_id>/

# پرداخت از سبد خرید
/payment/checkout/

# Callback زرین‌پال
/payment/callback/

# صفحه موفقیت
/payment/success/<payment_id>/

# صفحه شکست
/payment/failed/<payment_id>/
```

## 🧪 تست در حالت Sandbox

### کارت‌های تست:

برای تست موفق:
- شماره کارت: `5859831000000008`
- CVV2: هر عددی
- تاریخ انقضا: هر تاریخی در آینده
- رمز دوم: `123456`

برای تست ناموفق:
- شماره کارت: `5859831000000016`

## 📊 جریان کار

```
1. کاربر روی "پرداخت آنلاین" کلیک می‌کند
   └─> initiate_payment(plan_id)

2. درخواست به زرین‌پال ارسال می‌شود
   └─> دریافت Authority

3. هدایت به درگاه پرداخت
   └─> zarinpal.com/pg/StartPay/{authority}

4. کاربر پرداخت می‌کند
   └─> بازگشت به callback

5. تأیید پرداخت
   └─> verify با زرین‌پال

6. در صورت موفقیت:
   ├─> فعال‌سازی اشتراک
   ├─> خالی کردن سبد خرید
   └─> هدایت به payment_success

7. در صورت شکست:
   └─> هدایت به payment_failed
```

## ⚠️ نکات مهم

1. **Merchant ID واقعی**: در production حتماً Merchant ID واقعی استفاده کنید
2. **HTTPS**: در production حتماً از HTTPS استفاده کنید
3. **Callback URL**: باید از خارج قابل دسترسی باشد
4. **Webhook**: برای امنیت بیشتر، Webhook زرین‌پال را فعال کنید
5. **Logging**: تمام تراکنش‌ها log می‌شوند

## 🔐 امنیت

- تمام تراکنش‌ها در دیتابیس ذخیره می‌شوند
- IP کاربر ثبت می‌شود
- تأیید دوباره با verify
- CSRF protection فعال است
- شماره کارت 6 رقم اول ذخیره می‌شود

## 📞 پشتیبانی

مشکل در پرداخت؟
- لاگ‌ها را بررسی کنید: `logs/django.log`
- کد خطا را از پنل زرین‌پال بررسی کنید
- [مستندات API زرین‌پال](https://docs.zarinpal.com/)

