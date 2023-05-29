from .models import *
from django.contrib import admin


# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


class CustomersAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'email', 'phone', 'address')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_price', 'order_timestamp', 'payment_type', 'delivery_type')
    inlines = [ProductInOrderInline]
    list_filter = ['order_timestamp']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name')


class BasketAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'product', 'count', 'price_per_item', 'total_price', 'is_shown')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('status_id', 'status_name', 'is_active')


class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'count', 'total_price')


admin.site.register(Product, ProductAdmin)
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Orders, OrderAdmin)
admin.site.register(MeasuredUnit)
admin.site.register(Brand)
admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductInOrder, ProductInOrderAdmin)
admin.site.register(Basket, BasketAdmin)
