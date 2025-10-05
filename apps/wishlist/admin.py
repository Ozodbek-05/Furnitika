from django.contrib import admin

from django.contrib import admin
from .models import WishlistModel


@admin.register(WishlistModel)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product',)
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__title')
    ordering = ('-created_at',)
