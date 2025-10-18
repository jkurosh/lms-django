from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.case_list, name='case_list'),
    path('case/<int:case_id>/', views.case_detail, name='case_detail'),
    path('debug/<int:case_id>/', views.debug_case, name='debug_case'),
    path('category/<slug:category_slug>/', views.case_list, name='case_list_by_category'),
    
    # احراز هویت
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # پروفایل کاربر
    path('profile/', views.profile_view, name='profile'),
    
    # API endpoints
    path('save-progress/', views.save_progress, name='save_progress'),
    path('submit-result/', views.submit_case_result, name='submit_case_result'),
    path('api/default-options/', views.get_default_options, name='get_default_options'),
]