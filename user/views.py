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
        for item in items:
            print(item)
            shop = item.shop_id
            print(shop)
            shop_user_id  = User.objects.get(username = shop).id
            shop_info = Shop.objects.get(user = shop_user_id)
            shop_location =  {
                'shop_name':shop,
                'latitude' : shop_info.latitude, 
                            'longitude' : shop_info.longitude}
            location_data.append(shop_location)

        station_distance ={}

        for station in location_data:
            station_location = station['latitude'], station['longitude'] 
            distance  = geodesic(user_location,station_location).km
            station_distance[distance] = station_location

        min_distance = min(station_distance)
        station_cord = station_distance[min_distance]
        min_distance = round(min_distance, 3)


        return HttpResponse( shop )
        # return JsonResponse({
        #     'cord':station_cord,
        #     'distance':shop,
        # })
        # print(shop_info.latitude)
        #     print()
        # return HttpResponse()
    return render(request, 'userhome.html')