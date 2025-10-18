from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class OTPVerification(models.Model):
    """
    مدل ذخیره کدهای OTP
    """
    PURPOSE_CHOICES = [
        ('register', 'ثبت‌نام'),
        ('login', 'ورود'),
        ('password_reset', 'بازیابی رمز عبور'),
    ]
    
    phone_number = models.CharField(max_length=11, verbose_name='شماره موبایل')
    otp_code = models.CharField(max_length=6, verbose_name='کد تایید')
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, verbose_name='هدف')
    is_verified = models.BooleanField(default=False, verbose_name='تایید شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    expires_at = models.DateTimeField(verbose_name='تاریخ انقضا')
    attempts = models.IntegerField(default=0, verbose_name='تعداد تلاش')
    
    class Meta:
        app_label = 'apps.users'
        db_table = 'otp_verifications'
        verbose_name = 'کد تایید OTP'
        verbose_name_plural = 'کدهای تایید OTP'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone_number', 'purpose']),
            models.Index(fields=['expires_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # کد به مدت 5 دقیقه معتبر است
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        """
        بررسی انقضای کد
        """
        return timezone.now() > self.expires_at
    
    def increment_attempts(self):
        """
        افزایش تعداد تلاش‌ها
        """
        self.attempts += 1
        self.save()
    
    def __str__(self):
        return f"{self.phone_number} - {self.get_purpose_display()}"


class UserProfile(models.Model):
    """
    پروفایل کاربر با اطلاعات تکمیلی
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_profile')
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')
    is_phone_verified = models.BooleanField(default=False, verbose_name='موبایل تایید شده')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='تصویر پروفایل')
    bio = models.TextField(blank=True, verbose_name='بیوگرافی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        app_label = 'apps.users'
        db_table = 'user_profiles_auth'
        verbose_name = 'پروفایل کاربر (Auth)'
        verbose_name_plural = 'پروفایل‌های کاربر (Auth)'
    
    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"


class PurchaseNotification(models.Model):
    """
    مدل ذخیره اعلان‌های خرید
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms_purchase_notifications')
    phone_number = models.CharField(max_length=11, verbose_name='شماره موبایل')
    order_id = models.CharField(max_length=50, verbose_name='شماره سفارش')
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='مبلغ')
    is_sent = models.BooleanField(default=False, verbose_name='ارسال شده')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ ارسال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        app_label = 'apps.users'
        db_table = 'sms_purchase_notifications'
        verbose_name = 'اعلان خرید (SMS)'
        verbose_name_plural = 'اعلان‌های خرید (SMS)'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"سفارش {self.order_id} - {self.user.username}"
