from django.contrib import admin
from django.urls import URLResolver

from .models import AvatarC, AvatarP, Category, Producte, Comment, Buy

class AvatarCInline(admin.StackedInline):
    model = AvatarC
    fields = ['avatar']
    extra = 0

class AvatarPInline(admin.StackedInline):
    model = AvatarP
    fields = ['avatar']
    extra = 0

class CategoryInline(admin.StackedInline):
    model = Category
    extra = 0

class ProductInline(admin.StackedInline):
    model = Producte
    extra = 0
    fields = ['title', 'price', 'created_time']
    readonly_fields = ['created_time']


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    fields = ['user', 'describtion', 'created_time', 'producte']
    readonly_fields = ['created_time']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['parent', 'title', 'id']
    inlines = [AvatarCInline, CategoryInline, ProductInline]
    list_display_links = ['title']
    
@admin.register(Producte)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'created_time']
    inlines = [AvatarPInline, CommentInline]
    readonly_fields = ['created_time']

@admin.register(Buy)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'user']
