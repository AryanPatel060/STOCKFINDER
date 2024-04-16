from django.contrib import admin
from .models import Shop ,Item ,Item_Category


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['user','phone_no','latitude','longitude','shop_type', 'shopkeeper_name', 
                'shop_opening_time', 'shop_closing_time', 'shop_image', 'created_at', 'updated_at']

@admin.register(Item)    
class ItemAdmin(admin.ModelAdmin):
    list_display = ['shop_id', 'item_name','brand' , 'modal_no','price','quantity','item_image','created_at' ,'updated_at']
    
# 'Item_Category',
    
@admin.register(Item_Category)    
class Item_CategoryAdmin(admin.ModelAdmin):
    list_display = ['Category_name','price_type','created_at' ,'updated_at']

