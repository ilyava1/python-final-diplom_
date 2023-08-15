from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('backend_app.urls')),
    path('import/', include('import.urls')),
    path('admin/', admin.site.urls),
]
