from django.urls import path
from . import payment_api_views

app_name = 'payment_api'

urlpatterns = [
    # ایجاد و تایید پرداخت
    path('create/', payment_api_views.create_payment, name='create-payment'),
    path('verify/', payment_api_views.verify_payment, name='verify-payment'),
    
    # محاسبه کارمزد
    path('calculate-fee/', payment_api_views.calculate_fee, name='calculate-fee'),
    
    # لیست و جزئیات پرداخت‌ها
    path('list/', payment_api_views.payment_list, name='payment-list'),
    path('<int:payment_id>/', payment_api_views.payment_detail, name='payment-detail'),
]
