from django.urls import path
from . import views
from . import views_cart
from . import views_zarinpal

app_name = 'users'

urlpatterns = [
    path('', views.dadash_home, name='dadash_home'),
    path('landing/', views.landing_page, name='landing_page'),
    path('categories/', views.categories_page, name='categories_page'),
    path('api/categories/<int:category_id>/subcategories/', views.get_subcategories_api, name='get_subcategories_api'),
    
    # Bookmark APIs
    path('api/bookmark/<int:case_id>/toggle/', views.toggle_bookmark_api, name='toggle_bookmark_api'),
    path('api/bookmarks/', views.get_bookmarks_api, name='get_bookmarks_api'),
    path('api/bookmark/<int:case_id>/status/', views.check_bookmark_status_api, name='check_bookmark_status_api'),
    path('api/bookmark/<int:bookmark_id>/remove/', views.remove_bookmark_api, name='remove_bookmark_api'),
    path('categories-home/', views.categories_home, name='categories_home'),
    path('internal-diseases/', views.internal_diseases, name='internal_diseases'),
    path('surgery/', views.surgery, name='surgery'),
    path('emergency/', views.emergency, name='emergency'),
    path('dermatology/', views.dermatology, name='dermatology'),
    path('radiology/', views.radiology, name='radiology'),
    path('cardiology/', views.cardiology, name='cardiology'),
    
    # User Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('designali/', views.designali_dashboard, name='designali_dashboard'),
    path('profile/', views.designali_dashboard, name='profile'),  # همان صفحه designali با URL جدید
    path('my-cases/', views.my_cases, name='my_cases'),
    path('analytics/', views.analytics, name='analytics'),
    path('achievements/', views.achievements, name='achievements'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    
            # Authentication URLs
            path('login/', views.CustomLoginView.as_view(), name='login'),
            path('register/', views.register_view, name='register'),
            path('api/check-username/', views.check_username_availability, name='check_username'),
            path('api/check-phone/', views.check_phone_availability, name='check_phone'),
            path('logout/', views.logout_view, name='logout'),
            path('password-reset/', views.password_reset_view, name='password_reset'),
            path('password-reset/verify-phone/', views.verify_phone_api, name='verify_phone_api'),
            path('password-reset/verify-otp/', views.verify_otp_api, name='verify_otp_api'),
            path('password-reset/change-password/', views.change_password_api, name='change_password_api'),
    path('admin-panel/send-notification/', views.send_notification_view, name='send_notification'),
    path('admin-panel/notifications/', views.get_notifications_stats, name='notifications_stats'),
    path('user-notifications/', views.user_notifications_view, name='user_notifications'),
    path('user-notifications/<int:notification_id>/mark-read/', views.mark_notification_read_view, name='mark_notification_read'),
    path('user-notifications/mark-all-read/', views.mark_all_notifications_read_view, name='mark_all_notifications_read'),
    path('user-notifications/<int:notification_id>/delete/', views.delete_notification_view, name='delete_notification'),
    
    # Subscription Management
    path('subscription-status/', views.subscription_status, name='subscription_status'),
    
    # Security
    path('security-warning/', views.security_warning, name='security_warning'),
            
            # Admin Panel
            path('admin-panel/', views.admin_panel, name='admin_panel'),
    
    # سبد خرید
    path('cart/', views_cart.view_cart, name='view_cart'),
    path('cart/add/<int:plan_id>/', views_cart.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views_cart.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views_cart.update_cart_item, name='update_cart_item'),
    path('cart/clear/', views_cart.clear_cart, name='clear_cart'),
    path('api/cart-count/', views_cart.get_cart_count, name='get_cart_count'),
    
    # پلن‌های اشتراک و پرداخت
    path('subscription-plans/', views.subscription_plans_view, name='subscription_plans'),
    
    # پرداخت زرین‌پال
    path('payment/start/<int:plan_id>/', views_zarinpal.initiate_payment, name='initiate_payment'),
    path('payment/checkout/', views_zarinpal.checkout_from_cart, name='checkout'),
    path('payment/callback/', views_zarinpal.payment_callback, name='payment_callback'),
    path('payment/success/<int:payment_id>/', views_zarinpal.payment_success, name='payment_success'),
    path('payment/failed/<int:payment_id>/', views_zarinpal.payment_failed, name='payment_failed'),
] 