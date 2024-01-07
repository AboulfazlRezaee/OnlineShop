from django.contrib import admin

from .models import Product

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'active', 'datetime_created', 'datetime_modified',)