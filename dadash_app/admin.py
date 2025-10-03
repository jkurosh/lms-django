from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser, Notification, Subscription

# Unregister the default User model if it's registered
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """مدیریت کاربران سفارشی"""
    
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'email', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined', 'is_verified')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'phone_number', 'email')}),
        ('مجوزها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('اطلاعات امنیتی', {'fields': ('ip_address', 'successful_logins', 'failed_logins', 'devices', 'search_engine')}),
        ('تاریخ‌ها', {'fields': ('last_login', 'last_successful_login', 'last_failed_login', 'date_joined')}),
        ('تأیید', {'fields': ('is_verified', 'verification_code', 'verification_expires')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login', 'last_successful_login', 'last_failed_login', 'successful_logins', 'failed_logins')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """مدیریت اعلان‌ها"""
    
    list_display = ('title', 'notification_type', 'recipient_or_broadcast', 'is_read', 'is_active', 'created_at')
    list_filter = ('notification_type', 'is_read', 'is_active', 'is_broadcast', 'created_at')
    search_fields = ('title', 'message', 'recipient__username', 'recipient__first_name', 'recipient__last_name')
    ordering = ('-created_at',)
    actions = ['mark_as_read', 'mark_as_unread', 'send_broadcast']
    
    fieldsets = (
        ('اطلاعات اعلان', {
            'fields': ('title', 'message', 'notification_type')
        }),
        ('دریافت‌کنندگان', {
            'fields': ('is_broadcast', 'recipient'),
            'description': 'برای اعلان عمومی، is_broadcast را فعال کنید و recipient را خالی بگذارید'
        }),
        ('تنظیمات', {
            'fields': ('is_active', 'expires_at'),
            'classes': ('collapse',)
        }),
        ('اطلاعات فرستنده', {
            'fields': ('sender',),
            'classes': ('collapse',)
        }),
    )
    
    def recipient_or_broadcast(self, obj):
        """نمایش دریافت‌کننده یا اعلان عمومی"""
        if obj.is_broadcast:
            return "اعلان عمومی"
        return obj.recipient.get_full_name() if obj.recipient else "نامشخص"
    recipient_or_broadcast.short_description = 'دریافت‌کننده'
    
    @admin.action(description="علامت‌گذاری به عنوان خوانده شده")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} اعلان به عنوان خوانده شده علامت‌گذاری شد.')
    
    @admin.action(description="علامت‌گذاری به عنوان خوانده نشده")
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'{updated} اعلان به عنوان خوانده نشده علامت‌گذاری شد.')
    
    @admin.action(description="ارسال اعلان عمومی به همه کاربران")
    def send_broadcast(self, request, queryset):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        broadcast_count = 0
        for notification in queryset.filter(is_broadcast=False):
            # ایجاد کپی برای هر کاربر
            users = User.objects.filter(is_active=True)
            for user in users:
                Notification.objects.create(
                    title=notification.title,
                    message=notification.message,
                    notification_type=notification.notification_type,
                    recipient=user,
                    sender=request.user,
                    expires_at=notification.expires_at
                )
                broadcast_count += 1
        
        self.message_user(request, f'{broadcast_count} اعلان عمومی برای همه کاربران ارسال شد.')
    
    def save_model(self, request, obj, form, change):
        """ذخیره مدل با تنظیم فرستنده"""
        if not change:  # اگر جدید است
            obj.sender = request.user
        super().save_model(request, obj, form, change)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """مدیریت اشتراک‌ها"""
    
    list_display = ('user', 'subscription_type', 'status', 'start_date', 'end_date', 'price', 'days_remaining_display')
    list_filter = ('subscription_type', 'status', 'auto_renew', 'start_date', 'end_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'transaction_id')
    ordering = ('-created_at',)
    actions = ['activate_subscription', 'deactivate_subscription', 'extend_subscription_30_days', 'extend_subscription_90_days']
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user',)
        }),
        ('اطلاعات اشتراک', {
            'fields': ('subscription_type', 'status', 'end_date')
        }),
        ('اطلاعات پرداخت', {
            'fields': ('price', 'payment_method', 'transaction_id', 'auto_renew'),
            'classes': ('collapse',)
        }),
        ('یادداشت‌ها', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'start_date')
    
    def days_remaining_display(self, obj):
        """نمایش روزهای باقی‌مانده"""
        days = obj.days_remaining()
        if days is None:
            return "نامحدود"
        elif days == 0:
            return "منقضی شده"
        else:
            return f"{days} روز"
    days_remaining_display.short_description = 'روزهای باقی‌مانده'
    
    @admin.action(description="فعال کردن اشتراک")
    def activate_subscription(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} اشتراک فعال شد.')
    
    @admin.action(description="غیرفعال کردن اشتراک")
    def deactivate_subscription(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} اشتراک غیرفعال شد.')
    
    @admin.action(description="تمدید 30 روزه")
    def extend_subscription_30_days(self, request, queryset):
        count = 0
        for subscription in queryset:
            subscription.extend_subscription(30)
            count += 1
        self.message_user(request, f'{count} اشتراک 30 روز تمدید شد.')
    
    @admin.action(description="تمدید 90 روزه")
    def extend_subscription_90_days(self, request, queryset):
        count = 0
        for subscription in queryset:
            subscription.extend_subscription(90)
            count += 1
        self.message_user(request, f'{count} اشتراک 90 روز تمدید شد.')
