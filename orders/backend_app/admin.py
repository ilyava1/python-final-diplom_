from django.contrib import admin
from backend_app.models import User, Shop, Category, Product, ProductInfo
# from models import Parameter, ProductParameter, Order, OrderItem, Contact

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = 'username', 'email', 'is_active'
    list_filter = ['username']

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = 'name', 'url', 'filename'
    list_filter = ['name']