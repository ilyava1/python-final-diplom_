from django.urls import path
from .views import ShopView, CategoryView

urlpatterns = [
   path('shops/', ShopView.as_view()),
   path('shops/<pk>/', ShopView.as_view()),
   path('categories/', CategoryView.as_view()),
   ]