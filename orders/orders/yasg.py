from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='Дипломная работа к профессии Python-разработчик. '
              '«API Сервис заказа товаров для розничных сетей»',
        default_version='2.0',
        description='Приложение предназначено для автоматизации закупок'
                    ' в розничной сети. Пользователи сервиса — покупатель '
                    '(менеджер торговой сети, который закупает товары для '
                    'продажи в магазине) и поставщик товаров. '
                    'Приложение реализует backend-часть (Django) сервиса '
                    'заказа товаров для розничных сетей.',
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]