from django.db import models
from django.contrib.auth.models import User 


class Shop(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    phone_no = models.CharField(max_length=15, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    shop_type = models.CharField(max_length=100, null=True, blank=True)
    shopkeeper_name = models.CharField(max_length=255, null=True, blank=True)
    shop_opening_time = models.TimeField(null=True, blank=True)
    shop_closing_time = models.TimeField(null=True, blank=True)
    shop_image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username
    



class Item_Category(models.Model):
    IN_KG = 'FOR 1 KG'
    IN_LTR = 'FOR 1 LTR'
    PER_PIECE = 'PER PIECE'

    PRICE_CAT = [
        (IN_KG ,'FOR 1 KG'),
        (IN_LTR , 'FOR 1 LTR'),
        (PER_PIECE , 'PER PIECE'),
    ]
    Category_name =  models.CharField(max_length=50)
    price_type = models.CharField(max_length = 20 ,choices=PRICE_CAT,default = PER_PIECE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Category_name + " - "+self.price_type 



class Item(models.Model):

    shop_id= models.ForeignKey(Shop,on_delete  = models.CASCADE)
    item_name =  models.CharField(max_length=50)
    brand = models.CharField(max_length = 30,null = True , blank = True)
    modal_no = models.CharField(max_length  =30 ,null = True , blank = True)
    # Item_Category = models.ForeignKey(Item_Category , on_delete = models.SET('NONE'))
    price = models.FloatField(null=True)
    quantity = models.CharField(max_length = 30)
    item_image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_name

