from django.contrib import admin
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
    list_filter = ['brand']


class CustomersAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name',  'email', 'number', 'address')


class AdminAdmin(admin.ModelAdmin):
    fields = ['identifical_code', 'name', 'contact_email']
    list_display = ('identifical_code', 'name', 'contact_email')
    list_filter = ['name']


class BlackListAdmin(admin.ModelAdmin):
    list_display = ('reason', 'name_who_added', 'date')
    list_filter = ['date']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_timestamp', 'total_price', 'payment_type', 'delivery_type')
    inlines = [ProductInOrderInline]
    list_filter = ['order_timestamp']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name')

class BasketAdmin(admin.ModelAdmin):
    list_display = ('product', 'count' ,'price_per_item' , 'total_price', 'is_active')


admin.site.register(Product, ProductAdmin)
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(BlackList, BlackListAdmin)
admin.site.register(Orders, OrderAdmin)
admin.site.register(MeasuredUnit)
admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(Status)
admin.site.register(ProductImage)
admin.site.register(ProductInOrder)
admin.site.register(Basket, BasketAdmin)