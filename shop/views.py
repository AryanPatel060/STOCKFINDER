from django.shortcuts import render,HttpResponse,redirect
import shop.models as model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from shop.forms import AddShopDetails ,AddItem
import os
import datetime

def index(request):
    return render(request , 'index.html')

def loginshop(request):
       if request.user.username == 'admin' :
           return redirect('loginshop')
       if request.user.is_authenticated:
           return redirect("home")
       if request.method =="POST":
        email = request.POST.get('shopemail')
        password = request.POST.get('password')
        if not User.objects.filter(email = email).exists():
            messages.error(request,"Email does not exist.")
            return redirect(loginshop)
        else:
            shopname = User.objects.get(email=email).username
            shop_id = User.objects.get(email=email).id
            data = {
                'shopname':shopname,
                'shopeamil':email,
                'shop_id' : shop_id,
                # 'id': 2,
            }
            # shop = authenticate(username=email, password=password)
            shop  = User.objects.get(email = email)
            # password  = make_password(password)
           
            if(shop.password  == password ):
                request.session['shopdata'] = data
                login(request,shop)
                return redirect('AddShopData')
            else : 
                return redirect('loginshop')
            
       return render(request,'loginshop.html')




def signupshop(request):
    if request.user.is_authenticated:
           return redirect("home")
    if request.method =="POST":
        shopemail = request.POST.get('shopemail')
        password = request.POST.get('password')
        cpassword =request.POST.get('cpassword')
        shopname = request.POST.get('shopname')
        print(shopemail,password)
        # shop = authenticate(email = shopemail,password =password)
        shop = User.objects.filter(email = shopemail).exists()
        if(shop):
            messages.warning(request, 'email already exists.')
            return redirect(signupshop)
        if password == cpassword:
            # password = make_password(password)
            # password = make_password(password)
            shop = User.objects.create(username = shopname,email =  shopemail,password = password)
            model.Shop.objects.create(user = shop)
            messages.info( request,'signup successfully')
            return redirect('loginshop')
        else:
            messages.warning(request,'Passwords do not match')
            return redirect('signupshop')
    return render(request,'signupshop.html')



def logoutshop(request):
    logout(request)
    return redirect('loginshop')



@login_required(login_url="loginshop")
def home(request):
    if request.user.username == 'admin' :
        return redirect('loginshop')
    shop_id = request.session['shopdata']['shop_id']
    data = {}
    if model.Shop.objects.filter(user = shop_id).exists():
        shop_details = model.Shop.objects.get(user = shop_id)
        shop_data = True
        data = {
            'shop_details' :shop_details,
                }
    else :
        shop_data = False
    data['shop_data']= shop_data

    return render(request,'shopHome.html',context= data)


@login_required(login_url="loginshop")
def AddShopData(request):
    # form = AddShopDetails()
    shop_id = request.session['shopdata']['shop_id']
    shop = model.Shop.objects.get(user = shop_id)
    oldimg = False
    if shop.shop_image:
        print(shop.shop_image)
        oldImgURL = '.'+shop.shop_image.url  
        oldimg = True
        
    if request.method == "POST":
        form = AddShopDetails(request.POST ,request.FILES ,instance= shop)
        if model.Shop.objects.filter(user = shop_id).exists():
            mutable_querydict = form.data.copy()
            mutable_querydict['user'] =shop_id
            nf= False
            try:
                uploaded_file = request.FILES['shop_image']
                date = datetime.date.today()
                new_filename = str(shop_id)+'_shop_image'+str(date)+'.jpg'
                if uploaded_file:
                    nf = True
            except:
                pass
            form.data = mutable_querydict.copy()
            print(form.data)
        if form.is_valid():
            shop_instance = form.save(commit=False)
            if nf:  
                shop_instance.shop_image.save(new_filename, uploaded_file)
                if oldimg:
                    os.remove(oldImgURL)
            shop_instance.save()
            return redirect('home')
    else :
        form = AddShopDetails(instance= shop)
        data =  {
            'form':form
        }
        return render(request,'adddetails.html',context= data)
    
@login_required(login_url="loginshop")
def Additem(request):
    shop = request.session['shopdata']['shop_id']
    shop_id = model.Shop.objects.get(user = shop).id
    if request.method == 'POST':
        form = AddItem(request.POST , request.FILES)
        mutable_querydict = form.data.copy()
        mutable_querydict['shop_id'] =str(shop_id)
        uploaded_file = request.FILES['item_image']
        date = datetime.date.today()
        item_name= mutable_querydict['item_name'].lower()
        print(item_name)
        new_filename = str(shop_id)+'_'+item_name+'_item_image_'+str(date)+'.jpg'
        form.data = mutable_querydict.copy()
        print(form.data)
        if form.is_valid():
            shop_instance = form.save(commit=False)
            shop_instance.item_image.save(new_filename, uploaded_file)
            shop_instance.save()
            form.save()
    form = AddItem()
    items = model.Item.objects.filter(shop_id = shop_id)
    data={"items":items,"form":form}

    return render(request , 'additem.html', context = data)


@login_required(login_url="loginshop")
def deleteitem(request):
    if request.method == 'GET':
        item_id = request.GET.get('itemId')
        item = model.Item.objects.get(id = item_id)
        try:
            # item = model.Item.objects.filter(id = item_id)
            item_image_path = item.item_image.url
            if item_image_path != "" :
                os.unlink('.'+item_image_path)
            item.delete()
           
            shop = request.session['shopdata']['shop_id']
            shop_id = model.Shop.objects.get(user = shop).id
            form = AddItem()
            items = model.Item.objects.filter(shop_id = shop_id)
            data={"items":items,"form":form}
            return render(request , 'additem.html', context = data)
        except item.DoesNotExist:
            return JsonResponse({'error': 'Item does not exist'}, status=404)
    

 

    