from django.contrib import admin
from .models import CategoryModel, ManufacturerModel, ColorModel, TagModel, ProductModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title",)


@admin.register(ManufacturerModel)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title",)


@admin.register(ColorModel)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "code", "created_at")
    search_fields = ("title", "code")


@admin.register(TagModel)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title",)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "discount_price", "stock", "rating", "category", "manufacturer")
    list_filter = ("category", "manufacturer", "colors", "tags")
    search_fields = ("title", "description")
    filter_horizontal = ("colors", "tags")
