from django.contrib import admin
from backend_app.models import User, Contact


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = 'username', 'email', 'is_active'
    list_filter = ['username']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'user', 'value', 'type'
    list_filter = ['user']

