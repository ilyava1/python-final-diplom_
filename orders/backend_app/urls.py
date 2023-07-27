from django.urls import path
from .views import RegisterAccount, LoginAccount, ProductCatalog, ProductCard, product_view

urlpatterns = [
   path('user/register/', RegisterAccount.as_view()),
   path('user/login/', LoginAccount.as_view()),
   path('product/catalog/', ProductCatalog.as_view()),
   # path('product/catalog/<product_id>/', ProductCard.as_view()),
   path('product/catalog/<product_id>/', product_view),
   ]