from django.contrib import admin
from backend_app.models import User, Contact, Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = 'company_name', 'type', 'url', 'filename'
    list_filter = ['company_name']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = 'username', 'email', 'is_active'
    list_filter = ['username']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'user', 'value', 'company', 'position', 'phone'
    list_filter = ['user']

