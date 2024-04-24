from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from shop.models import Shop,Item,User
from geopy import distance as dst
from django.core.paginator import Paginator

# Create your views here.
def userhome(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        if  not search:
            return render(request, 'userhome.html')
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        user_location = latitude,longitude
        request.session["user_location"] = user_location
        items = Item.objects.filter(item_name__icontains=search)
        print(items)
        
        location_data = []
        location_data_without_img = []

        # p = Paginator(items, 1) 
        # page = request.GET.get('page')
        # shops = p.get_page(page)
        # print(shops)

        for item in items:
            # print(item.id)
            shop = item.shop_id
            item_img_url = item.item_image.url 
            item_id = item.id
            shop_user  = User.objects.get(username = shop)
            shop_user_id = shop_user.id
            shop_name  = shop_user.username
            shop_info = Shop.objects.get(user = shop_user_id)

            shop_location =  {
                'shop_id':shop_user_id,
                'shop_name':shop_name,
                'item_id':item_id,
                'latitude' : shop_info.latitude, 
                'longitude' : shop_info.longitude}
            
            location_data_without_img.append(shop_location)
            shop_location['item_img_url'] = item_img_url
            location_data.append(shop_location)

        station_distance ={}

        for station in location_data:
            station_location = station['latitude'], station['longitude'] 
            print (user_location , station_location)
            distance  = dst.distance(user_location,station_location).km
            print(station['shop_id'])
            distance = round(distance, 3)
            station_data  = { 'shop_name' : station['shop_name'],
                             'shop_id':station['shop_id'],
                             'item_id':station['item_id'],
                             'item_img_url' : station['item_img_url'],
                             'latitude' : station_location[0],
                             'longitude' : station_location[1]}
            
            station_distance[distance] = station_data
            # print(station_distance)


        # print(station_distance)
        sorted_location = dict(sorted(station_distance.items(), key=lambda item: item[0]))
        # print(sorted_location)
        return render(request  , 'userhome.html' , context= {'sorted_location'  : sorted_location , 'location_data' :location_data_without_img 
                                                            #  ,'products':shops
                                                             })
       
    return render(request, 'userhome.html')

def getroute(request):

    item_id= request.GET.get('item_id')
    item_info = Item.objects.get(id = item_id)
    # print(shop_id)
    shop_id = request.GET.get('shop_id')
    shop_info = Shop.objects.get(user = shop_id)
    user_location = request.session["user_location"]
    distance  = dst.distance(user_location,[shop_info.latitude,shop_info.longitude]).km
    distance = round(distance, 3)

    shop_location =  {
                    'shop_id':shop_id,
                    'latitude' : shop_info.latitude, 
                    'longitude' : shop_info.longitude,
                    'distance' : distance,
                    }
    
    return render(request, 'showroute.html' , context = {'shop_location':shop_location,'shop_info':shop_info,'item_info':item_info})

def getroute2(request):

    shop_id = request.GET.get('shop_id')
    shop_info = Shop.objects.get(user = shop_id)
    shop_location =  {
                    'shop_id':shop_id,
                    'latitude' : shop_info.latitude, 
                    'longitude' : shop_info.longitude}
    # return render(request, 'showroute.html' , context = {'shop_location':shop_location})
    return JsonResponse(shop_location)