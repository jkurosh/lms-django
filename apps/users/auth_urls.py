from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import auth_views

app_name = 'auth'

urlpatterns = [
    # ارسال و تایید OTP
    path('send-otp/', auth_views.send_otp, name='send-otp'),
    path('verify-otp/', auth_views.verify_otp, name='verify-otp'),
    
    # ثبت‌نام و ورود
    path('register/', auth_views.register, name='register'),
    path('login/', auth_views.login_with_otp, name='login'),
    
    # بازیابی رمز عبور
    path('password-reset/', auth_views.password_reset, name='password-reset'),
    
    # JWT Token Refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # اعلان خرید
    path('purchase/send-notification/', auth_views.send_purchase_notification, name='purchase-notification'),
    path('purchase/notifications/', auth_views.get_purchase_notifications, name='purchase-notifications-list'),
]
