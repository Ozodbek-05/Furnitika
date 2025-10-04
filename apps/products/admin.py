from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (
    ProductCategoryModel,
    ManufacturerModel,
    ColorModel,
    ProductTagModel,
    ProductModel,
    ProductImageModel, DealOfTheDayModel
)

class MyTranslationAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class ProductImageInline(admin.TabularInline):
    model = ProductImageModel
    extra = 2
    max_num = 5

@admin.register(ProductCategoryModel)
class CategoryAdmin(MyTranslationAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title",)


@admin.register(ManufacturerModel)
class ManufacturerAdmin(MyTranslationAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)


@admin.register(ColorModel)
class ColorAdmin(MyTranslationAdmin):
    list_display = ("id", "title", "code", "created_at")
    search_fields = ("title", "code")


@admin.register(ProductTagModel)
class TagAdmin(MyTranslationAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title",)


@admin.register(ProductModel)
class ProductAdmin(MyTranslationAdmin):
    inlines = [ProductImageInline]  # Inline qo‘shildi
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
    filter_horizontal = ("colors", "tags")  # rang va teglarni tanlash osonroq



@admin.register(DealOfTheDayModel)
class DealOfTheDayAdmin(admin.ModelAdmin):
    list_display = ("product", "deal_price", "start_time", "end_time", "is_active")
    list_filter = ("start_time", "end_time")
    search_fields = ("product__title",)
    ordering = ("-start_time",)

    readonly_fields = ("is_active",)