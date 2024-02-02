from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from .models import Product, Comment, Category

# Register your models here.

class CommentsInline(admin.StackedInline):
    model = Comment
    fields = ['author', 'body', 'stars', 'active', ]
    extra = 1

@admin.register(Product)
class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title', 'price', 'active', 'datetime_created', 'datetime_modified',)

    inlines = [
        CommentsInline,
        ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'body', 'stars', 'datetime_created', 'datetime_modified', 'active',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)