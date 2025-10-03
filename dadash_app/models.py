from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings

class CustomUser(AbstractUser):
    """مدل کاربر سفارشی با فیلدهای اضافی"""
    
    # فیلدهای اصلی
    first_name = models.CharField(max_length=100, verbose_name='نام')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    phone_number = models.CharField(max_length=20, unique=True, verbose_name='شماره تلفن')
    
    # فیلدهای امنیتی و پیگیری
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='آدرس IP')
    successful_logins = models.IntegerField(default=0, verbose_name='تعداد ورودهای موفق')
    failed_logins = models.IntegerField(default=0, verbose_name='تعداد ورودهای ناموفق')
    devices = models.JSONField(default=list, blank=True, verbose_name='دستگاه‌ها')
    search_engine = models.CharField(max_length=100, null=True, blank=True, verbose_name='موتور جستجو')
    
    # فیلدهای زمانی
    last_successful_login = models.DateTimeField(null=True, blank=True, verbose_name='آخرین ورود موفق')
    last_failed_login = models.DateTimeField(null=True, blank=True, verbose_name='آخرین ورود ناموفق')
    
    # فیلدهای اضافی
    is_verified = models.BooleanField(default=False, verbose_name='تأیید شده')
    verification_code = models.CharField(max_length=6, null=True, blank=True, verbose_name='کد تأیید')
    verification_expires = models.DateTimeField(null=True, blank=True, verbose_name='انقضای کد تأیید')
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    def get_full_name(self):
        """دریافت نام کامل کاربر"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def record_successful_login(self, ip_address=None, device_info=None):
        """ثبت ورود موفق"""
        self.successful_logins += 1
        self.last_successful_login = timezone.now()
        if ip_address:
            self.ip_address = ip_address
        if device_info:
            if device_info not in self.devices:
                self.devices.append(device_info)
        self.save(update_fields=['successful_logins', 'last_successful_login', 'ip_address', 'devices'])
    
    def record_failed_login(self, ip_address=None):
        """ثبت ورود ناموفق"""
        self.failed_logins += 1
        self.last_failed_login = timezone.now()
        if ip_address:
            self.ip_address = ip_address
        self.save(update_fields=['failed_logins', 'last_failed_login', 'ip_address'])
    
    def is_verification_code_valid(self, code):
        """بررسی اعتبار کد تأیید"""
        if not self.verification_code or not self.verification_expires:
            return False
        if self.verification_code != code:
            return False
        if timezone.now() > self.verification_expires:
            return False
        return True


class Subscription(models.Model):
    """مدل اشتراک کاربران"""
    
    SUBSCRIPTION_TYPES = [
        ('monthly', 'ماهانه'),
        ('quarterly', 'سه ماهه'),
        ('yearly', 'سالانه'),
        ('lifetime', 'مادام‌العمر'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'فعال'),
        ('expired', 'منقضی شده'),
        ('cancelled', 'لغو شده'),
        ('pending', 'در انتظار'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription', verbose_name='کاربر')
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES, default='monthly', verbose_name='نوع اشتراک')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ پایان')
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='قیمت')
    payment_method = models.CharField(max_length=50, blank=True, verbose_name='روش پرداخت')
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name='شناسه تراکنش')
    
    auto_renew = models.BooleanField(default=False, verbose_name='تمدید خودکار')
    notes = models.TextField(blank=True, verbose_name='یادداشت‌ها')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='زمان به‌روزرسانی')
    
    class Meta:
        verbose_name = 'اشتراک'
        verbose_name_plural = 'اشتراک‌ها'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_subscription_type_display()}"
    
    def is_active(self):
        """بررسی فعال بودن اشتراک"""
        if self.status != 'active':
            return False
        
        if self.end_date and timezone.now() > self.end_date:
            self.status = 'expired'
            self.save(update_fields=['status'])
            return False
        
        return True
    
    def days_remaining(self):
        """تعداد روزهای باقی‌مانده"""
        if not self.end_date:
            return None
        
        remaining = self.end_date - timezone.now()
        return max(0, remaining.days)
    
    def extend_subscription(self, days):
        """تمدید اشتراک به تعداد روز مشخص"""
        if self.end_date and self.end_date > timezone.now():
            # اگر اشتراک هنوز فعال است، از تاریخ پایان فعلی تمدید کن
            self.end_date += timezone.timedelta(days=days)
        else:
            # اگر اشتراک منقضی شده، از الان شروع کن
            self.end_date = timezone.now() + timezone.timedelta(days=days)
        
        self.status = 'active'
        self.save(update_fields=['end_date', 'status'])


class Notification(models.Model):
    """مدل اعلان برای کاربران"""
    
    NOTIFICATION_TYPES = [
        ('info', 'اطلاعاتی'),
        ('success', 'موفقیت'),
        ('warning', 'هشدار'),
        ('error', 'خطا'),
        ('announcement', 'اعلان عمومی'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='عنوان')
    message = models.TextField(verbose_name='پیام')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info', verbose_name='نوع اعلان')
    
    # دریافت‌کنندگان
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='دریافت‌کننده')
    is_broadcast = models.BooleanField(default=False, verbose_name='اعلان عمومی')
    
    # وضعیت
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    # زمان‌بندی
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='زمان خواندن')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='زمان انقضا')
    
    # فرستنده (اختیاری)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications', verbose_name='فرستنده')
    
    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلان‌ها'
        ordering = ['-created_at']
    
    def __str__(self):
        recipient_name = self.recipient.get_full_name() if self.recipient else "عمومی"
        return f"{self.title} - {recipient_name}"
    
    def mark_as_read(self):
        """علامت‌گذاری به عنوان خوانده شده"""
        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=['is_read', 'read_at'])
    
    def is_expired(self):
        """بررسی انقضای اعلان"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
