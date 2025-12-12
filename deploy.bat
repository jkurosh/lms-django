@echo off
chcp 65001 >nul
cls
echo ========================================
echo   Django VPS Deployment Script
echo   نصب و راه‌اندازی پروژه
echo ========================================
echo.

REM فعال کردن venv
echo [1/6] فعال‌سازی virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ خطا در فعال‌سازی venv!
    pause
    exit /b 1
)
echo ✅ venv فعال شد

echo.
REM نصب packages
echo [2/6] نصب packages...
pip install --upgrade pip
pip install -r requirements.txt
pip install waitress
if errorlevel 1 (
    echo ❌ خطا در نصب packages!
    pause
    exit /b 1
)
echo ✅ Packages نصب شد

echo.
REM Migration
echo [3/6] اجرای migrations...
python manage.py migrate --noinput
if errorlevel 1 (
    echo ❌ خطا در migration!
    pause
    exit /b 1
)
echo ✅ Migrations انجام شد

echo.
REM Collect static
echo [4/6] Collect کردن static files...
python manage.py collectstatic --noinput --clear
if errorlevel 1 (
    echo ❌ خطا در collectstatic!
    pause
    exit /b 1
)
echo ✅ Static files جمع‌آوری شد

echo.
REM بررسی فونت‌ها
echo [5/6] بررسی فونت‌ها...
dir staticfiles\fonts\bon-pro\
if errorlevel 1 (
    echo ⚠ پوشه فونت یافت نشد!
) else (
    echo ✅ فونت‌ها موجود است
)

echo.
echo [6/6] Deployment کامل شد!
echo.
echo ========================================
echo   آماده اجرا!
echo ========================================
echo.
echo دستورات اجرای سرور:
echo.
echo   1. برای port 80 (production):
echo      waitress-serve --host=0.0.0.0 --port=80 vetlms.wsgi:application
echo.
echo   2. برای port 8000 (test):
echo      waitress-serve --host=0.0.0.0 --port=8000 vetlms.wsgi:application
echo.
echo   3. برای اجرا در background:
echo      start /B waitress-serve --host=0.0.0.0 --port=80 vetlms.wsgi:application
echo.
echo ========================================
pause

