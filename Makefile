.PHONY: help build up down restart logs shell migrate collectstatic createsuperuser test clean backup restore

# رنگ‌ها برای خروجی
BLUE := \033[1;34m
GREEN := \033[1;32m
YELLOW := \033[1;33m
RED := \033[1;31m
NC := \033[0m # No Color

help: ## نمایش راهنمای دستورات
	@echo "$(BLUE)=== دستورات Docker برای VetLMS ===$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

setup: ## نصب اولیه - کپی env و ساخت کانتینرها
	@echo "$(BLUE)>>> کپی کردن فایل environment...$(NC)"
	@if not exist .env copy env.docker.example .env
	@echo "$(GREEN)✓ فایل .env ایجاد شد$(NC)"
	@echo "$(YELLOW)⚠ لطفاً فایل .env را ویرایش کنید$(NC)"

build: ## ساخت تصاویر Docker
	@echo "$(BLUE)>>> ساخت Docker images...$(NC)"
	docker-compose build
	@echo "$(GREEN)✓ ساخت تکمیل شد$(NC)"

up: ## اجرای کانتینرها در پس‌زمینه
	@echo "$(BLUE)>>> راه‌اندازی سرویس‌ها...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ سرویس‌ها راه‌اندازی شدند$(NC)"
	@echo "$(BLUE)سایت در دسترس است: http://localhost$(NC)"

down: ## توقف و حذف کانتینرها
	@echo "$(BLUE)>>> توقف سرویس‌ها...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ سرویس‌ها متوقف شدند$(NC)"

restart: ## ریستارت تمام سرویس‌ها
	@echo "$(BLUE)>>> ریستارت سرویس‌ها...$(NC)"
	docker-compose restart
	@echo "$(GREEN)✓ ریستارت انجام شد$(NC)"

logs: ## نمایش لاگ‌های تمام سرویس‌ها
	docker-compose logs -f

logs-web: ## نمایش لاگ‌های Django
	docker-compose logs -f web

logs-nginx: ## نمایش لاگ‌های Nginx
	docker-compose logs -f nginx

logs-db: ## نمایش لاگ‌های PostgreSQL
	docker-compose logs -f db

shell: ## ورود به shell Django container
	docker-compose exec web bash

shell-db: ## ورود به PostgreSQL shell
	docker-compose exec db psql -U vetlms_user -d vetlms_db

python-shell: ## ورود به Django Python shell
	docker-compose exec web python manage.py shell

migrate: ## اجرای مایگریشن‌ها
	@echo "$(BLUE)>>> اجرای migrations...$(NC)"
	docker-compose exec web python manage.py migrate
	@echo "$(GREEN)✓ Migrations اجرا شدند$(NC)"

makemigrations: ## ساخت migration جدید
	@echo "$(BLUE)>>> ساخت migrations...$(NC)"
	docker-compose exec web python manage.py makemigrations
	@echo "$(GREEN)✓ Migrations ساخته شدند$(NC)"

collectstatic: ## جمع‌آوری فایل‌های استاتیک
	@echo "$(BLUE)>>> جمع‌آوری static files...$(NC)"
	docker-compose exec web python manage.py collectstatic --noinput
	@echo "$(GREEN)✓ Static files جمع‌آوری شدند$(NC)"

createsuperuser: ## ساخت حساب سوپریوزر
	@echo "$(BLUE)>>> ساخت superuser...$(NC)"
	docker-compose exec web python manage.py createsuperuser

test: ## اجرای تست‌ها
	@echo "$(BLUE)>>> اجرای tests...$(NC)"
	docker-compose exec web python manage.py test

status: ## نمایش وضعیت کانتینرها
	@echo "$(BLUE)>>> وضعیت سرویس‌ها:$(NC)"
	@docker-compose ps

stats: ## نمایش آمار استفاده از منابع
	docker stats --no-stream

clean: ## پاک‌سازی volumes و توقف کامل
	@echo "$(RED)>>> حذف volumes و کانتینرها...$(NC)"
	@echo "$(YELLOW)⚠ این کار تمام داده‌ها را پاک می‌کند!$(NC)"
	@pause
	docker-compose down -v
	@echo "$(GREEN)✓ پاک‌سازی انجام شد$(NC)"

rebuild: down build up ## ساخت مجدد و اجرای کامل
	@echo "$(GREEN)✓ Rebuild کامل شد$(NC)"

backup-db: ## بکاپ از دیتابیس
	@echo "$(BLUE)>>> ایجاد backup...$(NC)"
	docker-compose exec db pg_dump -U vetlms_user vetlms_db > backup_$(shell powershell -Command "Get-Date -Format yyyyMMdd_HHmmss").sql
	@echo "$(GREEN)✓ Backup ایجاد شد$(NC)"

# دستور برای restore نیاز به نام فایل دارد: make restore-db FILE=backup.sql
restore-db: ## بازیابی دیتابیس از بکاپ
	@if "$(FILE)" == "" (echo "$(RED)خطا: نام فایل را مشخص کنید: make restore-db FILE=backup.sql$(NC)" && exit 1)
	@echo "$(BLUE)>>> بازیابی از $(FILE)...$(NC)"
	type $(FILE) | docker-compose exec -T db psql -U vetlms_user vetlms_db
	@echo "$(GREEN)✓ Restore انجام شد$(NC)"

install: setup build up migrate createsuperuser ## نصب کامل از ابتدا
	@echo "$(GREEN)✓✓✓ نصب با موفقیت انجام شد!$(NC)"
	@echo "$(BLUE)برنامه در http://localhost در دسترس است$(NC)"

update: ## بروزرسانی و ریستارت
	@echo "$(BLUE)>>> بروزرسانی...$(NC)"
	git pull
	docker-compose build
	docker-compose up -d
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py collectstatic --noinput
	@echo "$(GREEN)✓ بروزرسانی کامل شد$(NC)"

# دستور پیش‌فرض
.DEFAULT_GOAL := help

