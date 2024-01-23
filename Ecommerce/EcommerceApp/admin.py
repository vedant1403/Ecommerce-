from django.contrib import admin
from .models import Product,CartItem,Order

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    
    list_display=["wid","product_name","category","image","description","price"]

admin.site.register(Product,ProductAdmin)

class CartItemAdmin(admin.ModelAdmin):
    
    list_display=["product","quantity","user"]

admin.site.register(CartItem,CartItemAdmin)




class OrderAdmin(admin.ModelAdmin):
    
    list_display=["order_id","product_id","quantity","user","is_completed"]

admin.site.register(Order,OrderAdmin)


