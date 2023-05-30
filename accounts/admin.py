from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account
from products.admin import ProductInline, CommentInline

class AccountAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'phone_number', 'is_staff'
        )
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('avatar', 'first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
    )
    inlines = [ProductInline, CommentInline]

admin.site.register(Account, AccountAdmin)