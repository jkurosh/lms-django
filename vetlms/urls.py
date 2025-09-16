from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adlog/', admin.site.urls),
    path('', include('dadash_app.urls')),
    path('cases/', include('cases.urls')),
    path('api/v1/', include('cases.api_urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
