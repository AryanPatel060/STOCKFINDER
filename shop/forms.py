from django import forms
from django.forms import ModelForm
from shop.models import Shop ,Item

class AddShopDetails(ModelForm):
   class Meta:
        model = Shop
        # fields = ('user','shop_type', 'shopkeeper_name','phone_no','latitude','longitude','shop_opening_time','shop_closing_time')
        fields = '__all__'
        labels = {
            'user':'',
            'shop_image':'Shop Image'
        }
        widgets = {
            'user': forms.Select(attrs = {'class':'form-control','style':'display:none'}),
            'shop_type':forms.TextInput(attrs = {'class':'form-control',}), 
            'shopkeeper_name':forms.TextInput(attrs = {'class':'form-control',}),
            'phone_no':forms.TextInput(attrs = {'class':'form-control' ,}),
            'latitude':forms.TextInput(attrs = {'class':'form-control', 'type':'hidden'}),
            'longitude':forms.TextInput(attrs = {'class':'form-control' ,'type':'hidden'}),
            'shop_image':forms.FileInput(attrs = {'class':'form-control-file border','accept':'.jpg'}),
            'shop_opening_time':forms.TextInput(attrs = {'class':'form-control',}),
            'shop_closing_time':forms.TextInput(attrs = {'class':'form-control',}),
        }
       
class AddItem(ModelForm):
   class Meta:
        model = Item
        # fields = ('user','shop_type', 'shopkeeper_name','phone_no','latitude','longitude','shop_opening_time','shop_closing_time')
        fields = '__all__'
        labels = {
         
        }
        widgets = {
                    }
       