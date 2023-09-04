from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('api/', include('backend_app.urls')),
    path('import/', include('import.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += doc_urls