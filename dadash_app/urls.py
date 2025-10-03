from django.urls import path
from . import views

app_name = 'heyvoonak'

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
    path('my-cases/', views.my_cases, name='my_cases'),
    path('analytics/', views.analytics, name='analytics'),
    path('achievements/', views.achievements, name='achievements'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    
            # Authentication URLs
            path('login/', views.CustomLoginView.as_view(), name='login'),
            path('register/', views.register_view, name='register'),
            path('logout/', views.logout_view, name='logout'),
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
] 