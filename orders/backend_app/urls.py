from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import (RegisterAccount, AddToOrder, DelFromOrder, ViewOrder,
                    ViewOrderHistory, ChangeOrderStatus, ProductViewSet)
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'catalog', ProductViewSet, basename='product')

urlpatterns = [
    path('user/register/', RegisterAccount.as_view(), name = 'registration'),
    path('user/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('product/', include(router.urls)),
    path('product/order/add/<product_id>/<company_id>/<quantity>/',
         AddToOrder.as_view(), name='add_product_to_order'),
    path('product/order/delete/<order_id>/<product_id>/<company_id>/<quantity>/',
         DelFromOrder.as_view(), name='del_product_from_order'),
    path('product/order/view_order/<order_id>/', ViewOrder.as_view(), name='view_order'),
    path('product/order/view_order_history/', ViewOrderHistory.as_view(),
         name='order_history'),
    path('product/order/change_order_status/<order_id>/<order_status>/',
         ChangeOrderStatus.as_view()),
   ]