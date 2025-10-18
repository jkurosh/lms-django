from django.urls import path
from . import api_views

app_name = 'cases_api'

urlpatterns = [
    # Case endpoints
    path('cases/', api_views.CaseListView.as_view(), name='case-list'),
    path('cases/<int:pk>/', api_views.CaseDetailView.as_view(), name='case-detail'),
    path('cases/search/', api_views.search_cases, name='case-search'),
    path('cases/stats/', api_views.case_stats, name='case-stats'),
    
    # Category endpoints
    path('categories/', api_views.CategoryListView.as_view(), name='category-list'),
    
    # Lab test endpoints
    path('cases/<int:case_id>/lab-tests/', api_views.LabTestListView.as_view(), name='lab-test-list'),
    
    # User progress endpoints
    path('user-progress/', api_views.create_user_progress, name='create-user-progress'),
    path('user-progress/<int:user_id>/', api_views.user_progress_list, name='user-progress-list'),
    
    # User observation endpoints
    path('user-observations/', api_views.create_user_observation, name='create-user-observation'),
]
