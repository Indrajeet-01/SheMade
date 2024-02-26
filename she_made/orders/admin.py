from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'order_total', 'created_at']
    list_display_links = ['id', 'address']
    inlines = [OrderItemInline]

admin.site.register(OrderItem)
