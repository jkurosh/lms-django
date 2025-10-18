# راهنمای نصب در VPS ویندوز

## 📋 مراحل نصب

### 1️⃣ نصب Python

اگر Python نصب نیست:
```powershell
# دانلود Python 3.12 از python.org
# نصب با گزینه "Add to PATH"
```

### 2️⃣ نصب پکیج‌ها

**روش اول: نصب از requirements-vps.txt (توصیه می‌شود)**

```powershell
cd C:\Users\Administrator\vetlms
pip install --upgrade pip
pip install --only-binary :all: -r requirements-vps.txt
```

**روش دوم: نصب تک‌تک**

```powershell
pip install Django>=5.2.3
pip install psycopg2-binary
pip install Pillow
pip install whitenoise
pip install python-dotenv
pip install gunicorn
pip install dj-database-url
pip install djangorestframework
pip install django-cors-headers
pip install django-filter
pip install django-environ
pip install requests
pip install zarinpal
pip install jdatetime
```

### 3️⃣ پکیج‌های اختیاری

**اگر نیاز دارید:**

```powershell
# SMS (اختیاری)
pip install kavenegar

# امنیت (نیاز به Build Tools دارد)
pip install --only-binary cryptography cryptography

# Data Processing (سنگین - فقط در صورت نیاز)
pip install pandas
pip install openpyxl
```

### 4️⃣ اگر خطای Rust گرفتید

برای پکیج‌هایی که نیاز به Rust دارند:

```powershell
# فقط از binary wheels استفاده کنید
pip install --only-binary :all: cryptography
```

یا:

```powershell
# حذف cryptography از requirements اگر نیازی نیست
```

---

## 🔧 بررسی نصب

```powershell
# بررسی پکیج‌های نصب شده
pip list

# بررسی Django
python -m django --version

# تست سرور
python manage.py check
```

---

## 🚀 اجرای سرور

### Development:
```powershell
python manage.py runserver 0.0.0.0:8000
```

### Production (با Gunicorn):
```powershell
gunicorn vetlms.wsgi:application --bind 0.0.0.0:8000
```

---

## ⚠️ خطاهای رایج

### خطا: "No module named 'X'"
```powershell
# نصب پکیج مورد نظر
pip install [package-name]
```

### خطا: "Rust compiler not found"
```powershell
# استفاده از binary wheels
pip install --only-binary :all: [package-name]
```

### خطا: "metadata-generation-failed"
```powershell
# به‌روزرسانی pip
pip install --upgrade pip setuptools wheel
```

---

## 📝 نکات مهم

1. ✅ همیشه از **virtual environment** استفاده کنید
2. ✅ در VPS ویندوز از `requirements-vps.txt` استفاده کنید
3. ✅ پکیج‌های سنگین را فقط در صورت نیاز نصب کنید
4. ✅ برای production از **Gunicorn** یا **uWSGI** استفاده کنید
5. ✅ Static files را با `collectstatic` جمع‌آوری کنید

---

## 🔗 لینک‌های مفید

- Python: https://www.python.org/downloads/
- Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/
- Rust: https://rustup.rs/ (در صورت نیاز)
- Django Docs: https://docs.djangoproject.com/

---

## 💡 توصیه‌ها برای VPS

```powershell
# 1. ایجاد virtual environment
python -m venv venv
.\venv\Scripts\activate

# 2. نصب پکیج‌ها
pip install -r requirements-vps.txt

# 3. Migrate
python manage.py migrate

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. اجرای سرور
python manage.py runserver 0.0.0.0:8000
```

موفق باشید! 🎉


