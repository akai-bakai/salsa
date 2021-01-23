from django.contrib import admin

from .models import *

class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    max_num = 5
    min_num = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInLine, ]

admin.site.register(Category)
