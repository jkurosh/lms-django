"""
مدل‌های مربوط به پرداخت و تراکنش‌ها
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal


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
    
    # اطلاعات زرین‌پال
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
    
    # تاریخ‌ها
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان ایجاد'
    )
    
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='زمان پرداخت'
    )
    
    # اطلاعات اضافی
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
        
        # فعال‌سازی اشتراک
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

