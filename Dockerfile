# استفاده از Python 3.12 slim برای سبکی بیشتر
FROM python:3.12-slim

# تنظیم متغیرهای محیطی
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# تنظیم دایرکتوری کاری
WORKDIR /app

# نصب وابستگی‌های سیستمی برای PostgreSQL، Pillow و ابزارهای شبکه
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    netcat-traditional \
    curl \
    && rm -rf /var/lib/apt/lists/*

# کپی فایل requirements
COPY requirements.txt /app/

# نصب وابستگی‌های Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# کپی کد پروژه
COPY . /app/

# کپی و تنظیم entrypoint script
COPY entrypoint.sh /app/
COPY gunicorn.conf.py /app/
RUN chmod +x /app/entrypoint.sh

# ایجاد دایرکتوری‌های لازم
RUN mkdir -p /app/staticfiles /app/media /app/logs && \
    chmod -R 755 /app/staticfiles /app/media /app/logs

# تنظیم پورت
EXPOSE 8000

# اجرای entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

