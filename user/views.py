from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from shop.models import Shop,Item,User
from geopy.distance import geodesic
# Create your views here.

def userhome(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        user_location = latitude,longitude

        items = Item.objects.filter(item_name__icontains=search)

        location_data = []
        location_data_without_img = []
        for item in items:

            shop = item.shop_id
            item_img_url = item.item_image.url 

            shop_user  = User.objects.get(username = shop)
            shop_user_id = shop_user.id
            shop_name  = shop_user.username
            shop_info = Shop.objects.get(user = shop_user_id)

            shop_location =  {
                'shop_name':shop_name,
                'latitude' : shop_info.latitude, 
                'longitude' : shop_info.longitude}
            
            location_data_without_img.append(shop_location)
            shop_location['item_img_url'] = item_img_url
            location_data.append(shop_location)

        station_distance ={}

        for station in location_data:
            station_location = station['latitude'], station['longitude'] 
            distance  = geodesic(user_location,station_location).km
            distance = round(distance, 3)
            station_data  = { 'shop_name' : station['shop_name'],
                             'item_img_url' : station['item_img_url'],
                             'latitude' : station_location[0],
                             'longitude' : station_location[1]}
            
            station_distance[distance] = station_data


        # print(station_distance)
        sorted_location = dict(sorted(station_distance.items(), key=lambda item: item[0]))
        print(sorted_location)
        return render(request  , 'userhome.html' , context= {'sorted_location'  : sorted_location , 'location_data' :location_data_without_img })
        # min_distance = min(station_distance)
        # sorted_stations = (station_distance)
        # station_cord = station_distance[min_distance]
        # min_distance = round(min_distance, 3)

        # return HttpResponse(location_data)
        # return JsonResponse({
        #     'cord':station_cord,
        #     'distance':shop,
        # })
        # print(shop_info.latitude)
        #     print()
        # return HttpResponse()
    return render(request, 'userhome.html')