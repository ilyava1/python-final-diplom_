from django.urls import path
from .views import (RegisterAccount, LoginAccount, ProductCatalog,
                    ProductCard, AddToOrder, DelFromOrder, ViewOrder,
                    ViewOrderHistory, ChangeOrderStatus)

urlpatterns = [
    path('user/register/', RegisterAccount.as_view()),
    path('user/login/', LoginAccount.as_view()),
    path('product/catalog/', ProductCatalog.as_view()),
    path('product/catalog/<product_id>/', ProductCard.as_view()),
    path('product/catalog/add/<product_id>/<company_id>/<quantity>/',
         AddToOrder.as_view()),
    path('product/catalog/delete//<product_id>/<company_id>/<quantity>/',
         DelFromOrder.as_view()),
    path('product/catalog/view_order/<order_id>/', ViewOrder.as_view()),
    path('product/view_order_history/', ViewOrderHistory.as_view()),
    path('product/change_order_status/<order_id>/<order_status>/',
         ChangeOrderStatus.as_view()),
   ]