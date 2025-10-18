# 🗄️ راهنمای نصب و تنظیم MySQL برای پروژه VetLMS

## 📋 پیش‌نیازها

### 1. انتخاب نوع MySQL

#### **گزینه A: MySQL Local (Development)**
- **Windows:** [MySQL Installer](https://dev.mysql.com/downloads/installer/)
- **macOS:** `brew install mysql`
- **Ubuntu/Debian:** `sudo apt install mysql-server`

#### **گزینه B: Cloud MySQL (Production)**
- **Clever Cloud** (توصیه شده) - [clever-cloud.com](https://clever-cloud.com) - رایگان تا 1GB
- **PlanetScale:** [planetscale.com](https://planetscale.com) - رایگان تا 1GB
- **Railway:** [railway.app](https://railway.app) - رایگان تا 500MB
- **Supabase:** [supabase.com](https://supabase.com) - رایگان تا 500MB

### 2. نصب MySQL Client برای Python
```bash
pip install mysqlclient
```

## 🚀 مراحل راه‌اندازی

### مرحله 1: راه‌اندازی MySQL

#### **برای MySQL Local:**
```bash
# راه‌اندازی سرویس MySQL
sudo systemctl start mysql  # Linux
# یا در Windows از Services استفاده کنید

# ورود به MySQL
mysql -u root -p
```

#### **برای Cloud MySQL (Clever Cloud مثال):**
```bash
# 1. ثبت‌نام در clever-cloud.com
# 2. ایجاد MySQL Add-on جدید
# 3. کپی کردن Connection String
# 4. تنظیم Environment Variables
```

### مرحله 2: ایجاد دیتابیس
```sql
-- کپی کردن و اجرای محتوای فایل database_setup.sql
source /path/to/database_setup.sql;
```

### مرحله 3: تنظیم متغیرهای محیطی

#### **برای MySQL Local:**
فایل `.env` را در ریشه پروژه ایجاد کنید:
```env
# Database Configuration
DB_NAME=veterinary_cases
DB_USER=root
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=3306

# Use SQLite for development (set to 'true' to use SQLite instead of MySQL)
USE_SQLITE=false

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,::1
```

#### **برای Cloud MySQL (Clever Cloud):**
```env
# Database Configuration
DB_NAME=veterinary_cases
DB_USER=your_clever_cloud_user
DB_PASSWORD=your_clever_cloud_password
DB_HOST=your_clever_cloud_host.com
DB_PORT=3306

# Use SQLite for development (set to 'true' to use SQLite instead of MySQL)
USE_SQLITE=false

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.vercel.app
```

### مرحله 4: نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### مرحله 5: اجرای migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🔧 تنظیمات اضافی

### تنظیمات Vercel برای Clever Cloud MySQL
در Vercel Dashboard، Environment Variables زیر را اضافه کنید:
```env
USE_SQLITE=false
DB_NAME=veterinary_cases
DB_USER=your_clever_cloud_user
DB_PASSWORD=your_clever_cloud_password
DB_HOST=your_clever_cloud_host.com
DB_PORT=3306
```

### ایجاد کاربر جدید (اختیاری)
```sql
CREATE USER 'vetlms_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON veterinary_cases.* TO 'vetlms_user'@'localhost';
FLUSH PRIVILEGES;
```

### تنظیمات MySQL برای عملکرد بهتر
```sql
-- در فایل my.cnf یا my.ini
[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
default-storage-engine = InnoDB
innodb_buffer_pool_size = 256M
max_connections = 100
```

## 🧪 تست اتصال

### تست از طریق Django
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

### تست از طریق MySQL Client
```bash
mysql -u root -p -e "USE veterinary_cases; SHOW TABLES;"
```

## 🚨 حل مشکلات رایج

### مشکل 1: mysqlclient نصب نمی‌شود
```bash
# Windows
pip install --only-binary :all: mysqlclient

# macOS
brew install mysql-connector-c
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"
pip install mysqlclient

# Ubuntu/Debian
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

### مشکل 2: خطای اتصال
- بررسی کنید که MySQL سرویس در حال اجرا باشد
- رمز عبور را درست وارد کنید
- پورت 3306 باز باشد

### مشکل 3: خطای Character Set
```sql
ALTER DATABASE veterinary_cases CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 📊 ساختار دیتابیس

```
veterinary_cases/
├── category/           # دسته‌بندی‌های اصلی
├── sub_category/       # زیردسته‌ها
├── case_study/         # مطالعات موردی
├── case_test/          # تست‌های تشخیصی
├── case_option/        # گزینه‌های پاسخ
├── case_explanation/   # توضیحات
├── user/               # کاربران
└── user_progress/      # پیشرفت کاربران
```

## 🔄 بازگشت به SQLite

اگر می‌خواهید موقتاً از SQLite استفاده کنید:
```env
USE_SQLITE=true
```

## 📝 نکات مهم

1. **Backup:** همیشه از دیتابیس backup بگیرید
2. **Security:** کاربر root را فقط برای development استفاده کنید
3. **Performance:** از indexes استفاده کنید
4. **Unicode:** از utf8mb4 برای پشتیبانی کامل از emoji استفاده کنید

## 🚀 راهنمای سریع Clever Cloud

### مرحله 1: ثبت‌نام
1. به [clever-cloud.com](https://clever-cloud.com) بروید
2. با GitHub یا Google ثبت‌نام کنید
3. Plan رایگان را انتخاب کنید

### مرحله 2: ایجاد MySQL Add-on
1. روی "Create" کلیک کنید
2. "MySQL Add-on" را انتخاب کنید
3. نام `veterinary_cases` را وارد کنید
4. Region نزدیک به خود را انتخاب کنید

### مرحله 3: کپی کردن Connection Details
1. روی MySQL Add-on کلیک کنید
2. "Information" را انتخاب کنید
3. اطلاعات زیر را کپی کنید:
   - Host
   - Username
   - Password
   - Database name
   - Port

### مرحله 4: تنظیم Environment Variables
```env
DB_HOST=your_clever_cloud_host.com
DB_USER=your_clever_cloud_user
DB_PASSWORD=your_clever_cloud_password
DB_NAME=veterinary_cases
DB_PORT=3306
USE_SQLITE=false
```

## 🆘 پشتیبانی

اگر مشکلی داشتید:
1. لاگ‌های MySQL را بررسی کنید
2. Django debug mode را فعال کنید
3. اتصال دیتابیس را تست کنید
