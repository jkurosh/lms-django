from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser, Notification, Subscription, Payment, SubscriptionPlan, Cart, CartItem

# Unregister the default User model if it's registered
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """مدیریت کاربران سفارشی"""
    
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'email', 'subscription_status_display', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined', 'is_verified')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number', 'email')
    ordering = ('-date_joined',)
    
    def subscription_status_display(self, obj):
        """نمایش وضعیت اشتراک کاربر"""
        try:
            subscription = obj.subscription
            if subscription.status == 'active':
                from django.utils.html import format_html
                days = subscription.days_remaining()
                if days is None:
                    return format_html('<span style="color: green; font-weight: bold;">✓ فعال (نامحدود)</span>')
                elif days > 30:
                    return format_html('<span style="color: green; font-weight: bold;">✓ فعال ({} روز)</span>', days)
                elif days > 0:
                    return format_html('<span style="color: orange; font-weight: bold;">⚠ فعال ({} روز)</span>', days)
                else:
                    return format_html('<span style="color: red; font-weight: bold;">✗ منقضی شده</span>')
            elif subscription.status == 'pending':
                return format_html('<span style="color: blue;">⏳ در انتظار</span>')
            elif subscription.status == 'cancelled':
                return format_html('<span style="color: gray;">✗ لغو شده</span>')
            else:
                return format_html('<span style="color: red;">✗ منقضی</span>')
        except Subscription.DoesNotExist:
            return format_html('<span style="color: lightgray;">— بدون اشتراک</span>')
    subscription_status_display.short_description = 'وضعیت اشتراک'
    
    def get_inline_instances(self, request, obj=None):
        """اضافه کردن inline برای نمایش اشتراک"""
        if obj:
            return [SubscriptionInline(self.model, self.admin_site)]
        return []
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'phone_number', 'email')}),
        ('اشتراک', {'fields': ('subscription_info_display',), 'classes': ('collapse',)}),
        ('مجوزها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('اطلاعات امنیتی', {'fields': ('ip_address', 'successful_logins', 'failed_logins', 'devices', 'search_engine')}),
        ('تاریخ‌ها', {'fields': ('last_login', 'last_successful_login', 'last_failed_login', 'date_joined')}),
        ('تأیید', {'fields': ('is_verified', 'verification_code', 'verification_expires')}),
    )
    
    readonly_fields = ('date_joined', 'last_login', 'last_successful_login', 'last_failed_login', 'successful_logins', 'failed_logins', 'subscription_info_display')
    
    def subscription_info_display(self, obj):
        """نمایش اطلاعات کامل اشتراک"""
        try:
            subscription = obj.subscription
            from django.utils.html import format_html
            from django.urls import reverse
            url = reverse('admin:users_subscription_change', args=[subscription.pk])
            
            info = f"""
            <div style="padding: 10px; background: #f5f5f5; border-radius: 5px;">
                <p><strong>نوع اشتراک:</strong> {subscription.get_subscription_type_display()}</p>
                <p><strong>وضعیت:</strong> {subscription.get_status_display()}</p>
                <p><strong>تاریخ شروع:</strong> {subscription.start_date.strftime('%Y/%m/%d %H:%M') if subscription.start_date else '—'}</p>
                <p><strong>تاریخ پایان:</strong> {subscription.end_date.strftime('%Y/%m/%d %H:%M') if subscription.end_date else 'نامحدود'}</p>
                <p><strong>روزهای باقی‌مانده:</strong> {subscription.days_remaining() if subscription.days_remaining() is not None else 'نامحدود'}</p>
                <p><strong>قیمت:</strong> {subscription.price:,} تومان</p>
                <p style="margin-top: 10px;">
                    <a href="{url}" style="background: #417690; color: white; padding: 5px 15px; text-decoration: none; border-radius: 3px;">
                        ویرایش اشتراک
                    </a>
                </p>
            </div>
            """
            return format_html(info)
        except Subscription.DoesNotExist:
            from django.utils.html import format_html
            from django.urls import reverse
            url = reverse('admin:users_subscription_add') + f'?user={obj.pk}'
            return format_html(
                '<div style="padding: 10px; background: #fff3cd; border-radius: 5px;">'
                '<p>این کاربر هنوز اشتراکی ندارد.</p>'
                '<p><a href="{}" style="background: #28a745; color: white; padding: 5px 15px; text-decoration: none; border-radius: 3px;">'
                'ایجاد اشتراک جدید'
                '</a></p>'
                '</div>',
                url
            )
    subscription_info_display.short_description = 'جزئیات اشتراک'
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login', 'last_successful_login', 'last_failed_login', 'successful_logins', 'failed_logins', 'subscription_info_display')


# Inline برای نمایش اشتراک در صفحه کاربر
class SubscriptionInline(admin.StackedInline):
    """نمایش اشتراک به صورت inline"""
    model = Subscription
    extra = 0
    max_num = 1
    can_delete = True
    verbose_name = 'اشتراک کاربر'
    verbose_name_plural = 'اشتراک'
    
    fields = ('subscription_type', 'status', 'end_date', 'price', 'auto_renew', 'notes')
    readonly_fields = ('start_date', 'created_at', 'updated_at')


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
    
    list_display = ('user_full_name', 'subscription_type', 'status', 'start_date_display', 'end_date_display', 'price_display', 'days_remaining_display')
    list_filter = ('subscription_type', 'status', 'auto_renew', 'start_date', 'end_date', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'user__phone_number', 'transaction_id')
    ordering = ('-created_at',)
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    actions = [
        'activate_subscription', 
        'deactivate_subscription', 
        'cancel_subscription',
        'extend_subscription_30_days', 
        'extend_subscription_90_days',
        'extend_subscription_180_days',
        'extend_subscription_1_year',
        'set_lifetime',
        'delete_subscription'
    ]
    
    def user_full_name(self, obj):
        """نمایش نام کامل کاربر"""
        from django.utils.html import format_html
        from django.urls import reverse
        url = reverse('admin:users_customuser_change', args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.get_full_name() or obj.user.username)
    user_full_name.short_description = 'کاربر'
    user_full_name.admin_order_field = 'user__last_name'
    
    def status_display(self, obj):
        """نمایش رنگی وضعیت"""
        from django.utils.html import format_html
        colors = {
            'active': 'green',
            'pending': 'blue',
            'expired': 'red',
            'cancelled': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_status_display())
    status_display.short_description = 'وضعیت'
    status_display.admin_order_field = 'status'
    
    def start_date_display(self, obj):
        """نمایش فرمت شده تاریخ شروع"""
        if obj.start_date:
            return obj.start_date.strftime('%Y/%m/%d - %H:%M')
        return '—'
    start_date_display.short_description = 'تاریخ شروع'
    start_date_display.admin_order_field = 'start_date'
    
    def end_date_display(self, obj):
        """نمایش فرمت شده تاریخ پایان"""
        if obj.end_date:
            return obj.end_date.strftime('%Y/%m/%d - %H:%M')
        return 'نامحدود'
    end_date_display.short_description = 'تاریخ پایان'
    end_date_display.admin_order_field = 'end_date'
    
    def price_display(self, obj):
        """نمایش فرمت شده قیمت"""
        return f"{obj.price:,} تومان"
    price_display.short_description = 'قیمت'
    price_display.admin_order_field = 'price'
    
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
    
    @admin.action(description="غیرفعال کردن اشتراک (منقضی)")
    def deactivate_subscription(self, request, queryset):
        updated = queryset.update(status='expired')
        self.message_user(request, f'{updated} اشتراک غیرفعال شد.')
    
    @admin.action(description="لغو اشتراک")
    def cancel_subscription(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} اشتراک لغو شد.')
    
    @admin.action(description="🔄 تمدید 30 روزه")
    def extend_subscription_30_days(self, request, queryset):
        count = 0
        for subscription in queryset:
            subscription.extend_subscription(30)
            count += 1
        self.message_user(request, f'{count} اشتراک 30 روز تمدید شد.')
    
    @admin.action(description="🔄 تمدید 90 روزه (3 ماه)")
    def extend_subscription_90_days(self, request, queryset):
        count = 0
        for subscription in queryset:
            subscription.extend_subscription(90)
            count += 1
        self.message_user(request, f'{count} اشتراک 90 روز تمدید شد.')
    
    @admin.action(description="🔄 تمدید 180 روزه (6 ماه)")
    def extend_subscription_180_days(self, request, queryset):
        count = 0
        for subscription in queryset:
            subscription.extend_subscription(180)
            count += 1
        self.message_user(request, f'{count} اشتراک 180 روز تمدید شد.')
    
    @admin.action(description="🔄 تمدید 1 ساله (365 روز)")
    def extend_subscription_1_year(self, request, queryset):
        count = 0
        for subscription in queryset:
            subscription.extend_subscription(365)
            count += 1
        self.message_user(request, f'{count} اشتراک یک سال تمدید شد.')
    
    @admin.action(description="♾️ تبدیل به مادام‌العمر")
    def set_lifetime(self, request, queryset):
        count = 0
        for subscription in queryset:
            subscription.subscription_type = 'lifetime'
            subscription.end_date = None
            subscription.status = 'active'
            subscription.save()
            count += 1
        self.message_user(request, f'{count} اشتراک به مادام‌العمر تبدیل شد.')
    
    @admin.action(description="🗑️ حذف اشتراک")
    def delete_subscription(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} اشتراک حذف شد.')


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """مدیریت پلن‌های اشتراک"""
    
    list_display = ('name', 'duration_type', 'duration_days', 'formatted_price', 'discount_percent', 'is_popular', 'is_active', 'order')
    list_filter = ('duration_type', 'is_active', 'is_popular', 'created_at')
    search_fields = ('name', 'features')
    ordering = ('order', 'price')
    list_editable = ('is_active', 'is_popular', 'order')
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'duration_type', 'duration_days')
        }),
        ('قیمت‌گذاری', {
            'fields': ('price', 'discount_percent')
        }),
        ('ویژگی‌ها', {
            'fields': ('features',),
            'description': 'هر خط یک ویژگی'
        }),
        ('تنظیمات نمایش', {
            'fields': ('is_active', 'is_popular', 'order')
        }),
    )
    
    readonly_fields = ('created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """مدیریت پرداخت‌ها"""
    
    list_display = ('user', 'formatted_amount', 'gateway', 'status', 'ref_id', 'created_at', 'paid_at')
    list_filter = ('gateway', 'status', 'created_at', 'paid_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'authority', 'ref_id', 'transaction_id')
    ordering = ('-created_at',)
    actions = ['mark_as_paid', 'mark_as_failed']
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user', 'subscription')
        }),
        ('اطلاعات پرداخت', {
            'fields': ('amount', 'gateway', 'status')
        }),
        ('اطلاعات درگاه', {
            'fields': ('authority', 'ref_id', 'card_number'),
            'classes': ('collapse',)
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'paid_at'),
            'classes': ('collapse',)
        }),
        ('توضیحات', {
            'fields': ('description', 'ip_address'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'paid_at')
    
    @admin.action(description="علامت‌گذاری به عنوان پرداخت شده")
    def mark_as_paid(self, request, queryset):
        count = 0
        for payment in queryset.filter(status='pending'):
            payment.mark_as_paid(ref_id=f"ADMIN_{payment.id}")
            count += 1
        self.message_user(request, f'{count} پرداخت به عنوان پرداخت شده علامت‌گذاری شد.')
    
    @admin.action(description="علامت‌گذاری به عنوان ناموفق")
    def mark_as_failed(self, request, queryset):
        count = 0
        for payment in queryset.filter(status='pending'):
            payment.mark_as_failed()
            count += 1
        self.message_user(request, f'{count} پرداخت به عنوان ناموفق علامت‌گذاری شد.')


class CartItemInline(admin.TabularInline):
    """نمایش آیتم‌های سبد خرید به صورت inline"""
    model = CartItem
    extra = 0
    readonly_fields = ('added_at',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """مدیریت سبدهای خرید"""
    
    list_display = ('user', 'items_count', 'total_price', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at', 'total_price', 'items_count')
    inlines = [CartItemInline]
    
    fieldsets = (
        ('اطلاعات سبد', {
            'fields': ('user', 'created_at', 'updated_at')
        }),
        ('خلاصه', {
            'fields': ('items_count', 'total_price')
        }),
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """مدیریت آیتم‌های سبد خرید"""
    
    list_display = ('cart', 'plan', 'quantity', 'total_price', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('cart__user__username', 'plan__name')
    ordering = ('-added_at',)
