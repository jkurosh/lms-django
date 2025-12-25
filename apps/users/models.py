from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
from datetime import timedelta

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
            self.end_date += timedelta(days=days)
        else:
            # اگر اشتراک منقضی شده، از الان شروع کن
            self.end_date = timezone.now() + timedelta(days=days)
        
        self.status = 'active'
        self.save(update_fields=['end_date', 'status'])
    
    def activate(self, duration_days=30):
        """فعال‌سازی اشتراک"""
        self.status = 'active'
        self.start_date = timezone.now()
        self.end_date = timezone.now() + timedelta(days=duration_days)
        self.save()


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
    

class Payment(models.Model):
    """مدل پرداخت"""
    
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('failed', 'ناموفق'),
        ('cancelled', 'لغو شده'),
        ('refunded', 'بازگشت داده شده'),
    ]
    
    GATEWAY_CHOICES = [
        ('zarinpal', 'زرین‌پال'),
        ('manual', 'دستی'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='کاربر'
    )
    
    subscription = models.ForeignKey(
        'Subscription',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='اشتراک'
    )
    
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name='مبلغ (تومان)'
    )
    
    gateway = models.CharField(
        max_length=20,
        choices=GATEWAY_CHOICES,
        default='zarinpal',
        verbose_name='درگاه پرداخت'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='وضعیت'
    )
    
    authority = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Authority کد'
    )
    
    ref_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='شماره پیگیری'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان ایجاد'
    )
    
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='زمان پرداخت'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='توضیحات'
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='آدرس IP'
    )
    
    card_number = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        verbose_name='شماره کارت'
    )
    
    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت‌ها'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['authority']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} تومان - {self.get_status_display()}"
    
    def mark_as_paid(self, ref_id, card_number=None):
        """علامت‌گذاری به عنوان پرداخت شده"""
        self.status = 'paid'
        self.ref_id = ref_id
        self.paid_at = timezone.now()
        if card_number:
            self.card_number = card_number
        self.save()
        
        if self.subscription:
            self.subscription.activate()
    
    def mark_as_failed(self):
        """علامت‌گذاری به عنوان ناموفق"""
        self.status = 'failed'
        self.save()
    
    @property
    def is_paid(self):
        """آیا پرداخت شده است؟"""
        return self.status == 'paid'
    
    @property
    def formatted_amount(self):
        """مبلغ فرمت شده"""
        return f"{self.amount:,} تومان"


class SubscriptionPlan(models.Model):
    """پلن‌های اشتراک"""
    
    DURATION_CHOICES = [
        ('monthly', 'یک ماهه'),
        ('quarterly', 'سه ماهه'),
        ('biannual', 'شش ماهه'),
        ('yearly', 'یک ساله'),
        ('lifetime', 'مادام‌العمر'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name='نام پلن'
    )
    
    duration_type = models.CharField(
        max_length=20,
        choices=DURATION_CHOICES,
        verbose_name='نوع مدت'
    )
    
    duration_days = models.IntegerField(
        verbose_name='تعداد روز'
    )
    
    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name='قیمت (تومان)'
    )
    
    discount_percent = models.IntegerField(
        default=0,
        verbose_name='درصد تخفیف'
    )
    
    features = models.TextField(
        help_text='ویژگی‌ها (هر خط یک ویژگی)',
        verbose_name='ویژگی‌ها'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )
    
    is_popular = models.BooleanField(
        default=False,
        verbose_name='محبوب'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='ترتیب نمایش'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان ایجاد'
    )
    
    class Meta:
        verbose_name = 'پلن اشتراک'
        verbose_name_plural = 'پلن‌های اشتراک'
        ordering = ['order', 'price']
    
    def __str__(self):
        return f"{self.name} - {self.get_duration_type_display()}"
    
    @property
    def final_price(self):
        """قیمت نهایی با تخفیف"""
        if self.discount_percent > 0:
            discount_amount = (self.price * Decimal(self.discount_percent)) / Decimal(100)
            return self.price - discount_amount
        return self.price
    
    @property
    def formatted_price(self):
        """قیمت فرمت شده"""
        return f"{self.price:,}"
    
    @property
    def formatted_final_price(self):
        """قیمت نهایی فرمت شده"""
        return f"{self.final_price:,}"
    
    def get_features_list(self):
        """لیست ویژگی‌ها"""
        return [f.strip() for f in self.features.split('\n') if f.strip()]


class Cart(models.Model):
    """سبد خرید کاربر"""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='کاربر'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان ایجاد'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='زمان به‌روزرسانی'
    )
    
    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'
    
    def __str__(self):
        return f"سبد خرید {self.user.username}"
    
    @property
    def total_price(self):
        """مجموع قیمت سبد"""
        return sum(item.total_price for item in self.items.all())
    
    @property
    def items_count(self):
        """تعداد آیتم‌های سبد"""
        return self.items.count()
    
    @property
    def is_empty(self):
        """آیا سبد خالی است؟"""
        return self.items.count() == 0
    
    def clear(self):
        """خالی کردن سبد"""
        self.items.all().delete()


class CartItem(models.Model):
    """آیتم سبد خرید"""
    
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='سبد خرید'
    )
    
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        verbose_name='پلن اشتراک'
    )
    
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='تعداد'
    )
    
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان افزودن'
    )
    
    class Meta:
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم‌های سبد خرید'
        unique_together = ('cart', 'plan')
        indexes = [
            models.Index(fields=['cart']),  # برای فیلتر بر اساس cart
            models.Index(fields=['plan']),  # برای فیلتر بر اساس plan
        ]
    
    def __str__(self):
        return f"{self.plan.name} - {self.quantity}x"
    
    @property
    def total_price(self):
        """قیمت کل این آیتم"""
        return self.plan.final_price * self.quantity


class OTPVerification(models.Model):
    """
    مدل ذخیره کدهای OTP برای تایید شماره موبایل و بازیابی رمز
    """
    PURPOSE_CHOICES = [
        ('register', 'ثبت‌نام'),
        ('login', 'ورود'),
        ('password_reset', 'بازیابی رمز عبور'),
    ]
    
    phone_number = models.CharField(max_length=11, verbose_name='شماره موبایل')
    code = models.CharField(max_length=6, verbose_name='کد تایید')
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, verbose_name='هدف')
    is_verified = models.BooleanField(default=False, verbose_name='تایید شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    verified_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ تایید')
    expires_at = models.DateTimeField(verbose_name='تاریخ انقضا')
    attempts = models.IntegerField(default=0, verbose_name='تعداد تلاش')
    
    class Meta:
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
            # کد به مدت 2 دقیقه معتبر است
            self.expires_at = timezone.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        """بررسی انقضای کد"""
        return timezone.now() > self.expires_at
    
    def increment_attempts(self):
        """افزایش تعداد تلاش‌ها"""
        self.attempts += 1
        self.save()
    
    def __str__(self):
        return f"{self.phone_number} - {self.get_purpose_display()}"
