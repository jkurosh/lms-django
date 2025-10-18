# 🚀 راهنمای تنظیم MySQL در Vercel

## 📋 پیش‌نیازها

### 1. انتخاب Cloud MySQL Provider
- **Clever Cloud** (توصیه شده) - [clever-cloud.com](https://clever-cloud.com) - رایگان تا 1GB
- **PlanetScale** - رایگان تا 1GB
- **Railway** - رایگان تا 500MB
- **Supabase** - رایگان تا 500MB

## 🎯 مراحل راه‌اندازی

### مرحله 1: ایجاد Cloud MySQL Database

#### **Clever Cloud (توصیه شده):**
1. به [clever-cloud.com](https://clever-cloud.com) بروید
2. با GitHub یا Google ثبت‌نام کنید
3. Plan رایگان را انتخاب کنید
4. MySQL Add-on جدید با نام `veterinary_cases` ایجاد کنید
5. Region نزدیک به خود را انتخاب کنید

### مرحله 2: کپی کردن Connection Details

#### **از Clever Cloud:**
1. روی MySQL Add-on کلیک کنید
2. "Information" را انتخاب کنید
3. اطلاعات زیر را کپی کنید:
   - Host: `your_clever_cloud_host.com`
   - Username: `your_username`
   - Password: `your_password`
   - Database: `veterinary_cases`
   - Port: `3306`

### مرحله 3: تنظیم Environment Variables در Vercel

#### **در Vercel Dashboard:**
1. به پروژه خود در Vercel بروید
2. "Settings" را انتخاب کنید
3. "Environment Variables" را انتخاب کنید
4. متغیرهای زیر را اضافه کنید:

```env
USE_SQLITE=false
DB_NAME=veterinary_cases
DB_USER=your_clever_cloud_username
DB_PASSWORD=your_clever_cloud_password
DB_HOST=your_clever_cloud_host.com
DB_PORT=3306
```

### مرحله 4: اجرای Database Setup

#### **در Clever Cloud:**
1. "Console" را انتخاب کنید
2. محتوای فایل `database_setup.sql` را کپی کنید
3. Execute کنید

#### **یا از طریق MySQL Client:**
```bash
mysql -h your_clever_cloud_host.com -u your_username -p veterinary_cases < database_setup.sql
```

### مرحله 5: Deploy مجدد در Vercel

1. تغییرات را در GitHub push کنید
2. Vercel به صورت خودکار deploy می‌کند
3. Environment Variables جدید اعمال می‌شوند

## 🔧 تنظیمات اضافی

### SSL Configuration (برای Clever Cloud)
```env
DB_SSL_MODE=REQUIRED
```

### Connection Pooling (اختیاری)
```env
DB_MAX_CONNECTIONS=10
DB_CONNECTION_TIMEOUT=30
```

## 🧪 تست اتصال

### تست از طریق Django Shell:
```bash
python manage.py shell
```
```python
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT VERSION()")
version = cursor.fetchone()
print(f"MySQL Version: {version[0]}")
```

### تست از طریق MySQL Client:
```bash
mysql -h your_clever_cloud_host.com -u your_username -p veterinary_cases -e "SHOW TABLES;"
```

## 🚨 حل مشکلات رایج

### مشکل 1: خطای اتصال
- بررسی کنید که Environment Variables درست تنظیم شده باشند
- رمز عبور را درست وارد کنید
- Host و Port را بررسی کنید

### مشکل 2: خطای SSL
```env
DB_SSL_MODE=VERIFY_IDENTITY
```

### مشکل 3: خطای Character Set
```sql
ALTER DATABASE veterinary_cases CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 📊 ساختار Environment Variables

### **Development (.env):**
```env
USE_SQLITE=false
DB_NAME=veterinary_cases
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

### **Production (Vercel):**
```env
USE_SQLITE=false
DB_NAME=veterinary_cases
DB_USER=your_clever_cloud_user
DB_PASSWORD=your_clever_cloud_password
DB_HOST=your_clever_cloud_host.com
DB_PORT=3306
```

## 🔄 بازگشت به SQLite

اگر مشکلی پیش آمد:
```env
USE_SQLITE=true
```

## 📝 نکات مهم

1. **Security:** رمزهای عبور را در GitHub commit نکنید
2. **Backup:** همیشه از دیتابیس backup بگیرید
3. **Monitoring:** عملکرد دیتابیس را بررسی کنید
4. **Scaling:** در صورت نیاز به Plan بالاتر ارتقا دهید

## 🆘 پشتیبانی

### **Clever Cloud:**
- [Documentation](https://www.clever-cloud.com/doc/)
- [Support](https://www.clever-cloud.com/support/)

### **Vercel:**
- [Documentation](https://vercel.com/docs)
- [Support](https://vercel.com/support)

### **Django:**
- [Database Documentation](https://docs.djangoproject.com/en/stable/ref/databases/)
- [MySQL Backend](https://docs.djangoproject.com/en/stable/ref/databases/#mysql-notes)
