from django.urls import path
from . import views

app_name = 'heyvoonak'

urlpatterns = [
    path('', views.dadash_home, name='dadash_home'),
    path('internal-diseases/', views.internal_diseases, name='internal_diseases'),
    path('surgery/', views.surgery, name='surgery'),
    path('emergency/', views.emergency, name='emergency'),
    path('dermatology/', views.dermatology, name='dermatology'),
    path('radiology/', views.radiology, name='radiology'),
    path('cardiology/', views.cardiology, name='cardiology'),
] 