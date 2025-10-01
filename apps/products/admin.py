from django.contrib import admin
from .models import (
    ProductCategoryModel,
    ManufacturerModel,
    ColorModel,
    ProductTagModel,
    ProductModel,
    ProductImageModel, DealOfTheDayModel
)

# Inline for multiple images
class ProductImageInline(admin.TabularInline):
    model = ProductImageModel
    extra = 2  # boshlang'ichda 2 rasm qo'shish
    max_num = 5

@admin.register(ProductCategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title",)


@admin.register(ManufacturerModel)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)


@admin.register(ColorModel)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "code", "created_at")
    search_fields = ("title", "code")


@admin.register(ProductTagModel)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title",)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = (
        "id",
        "title",
        "price",
        "discount_price",
        "stock",
        "rating",
        "category",
        "manufacturer",
    )
    list_filter = ("category", "manufacturer", "colors", "tags")
    search_fields = ("title", "description")
    filter_horizontal = ("colors", "tags")


@admin.register(DealOfTheDayModel)
class DealOfTheDayAdmin(admin.ModelAdmin):
    list_display = ("product", "deal_price", "start_time", "end_time", "is_active")
    list_filter = ("start_time", "end_time")
    search_fields = ("product__title",)
    ordering = ("-start_time",)

    readonly_fields = ("is_active",)