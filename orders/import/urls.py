from django.urls import path
from .views import PriceImport

urlpatterns = [
   path('price_import/', PriceImport.as_view(), name='price-import'),
   ]