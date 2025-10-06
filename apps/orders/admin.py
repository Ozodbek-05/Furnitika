from django.contrib import admin
from apps.orders.models import OrderModel, OrderItemModel

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'unique_id', 'user', 'city', 'district',
        'total_price', 'total_products', 'payment_status', 'created_at'
    )
    list_filter = ('city', 'district', 'payment_status', 'created_at')
    search_fields = ('unique_id', 'user__username', 'city', 'district')
    ordering = ('-created_at',)
    readonly_fields = ('unique_id', 'total_price', 'total_products', 'created_at', 'updated_at')

    fieldsets = (
        ('Order Info', {
            'fields': ('unique_id', 'user', 'total_price', 'total_products', 'payment_status', 'payment_method')
        }),
        ('Address', {
            'fields': ('city', 'district', 'street', 'home_number', 'additional_info')
        }),
        ('Notes', {
            'fields': ('note',)
        }),
        ('System', {
            'fields': ('created_at', 'updated_at')
        }),
    )
