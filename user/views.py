from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
from shop.models import Shop,Item,User
# Create your views here.

def userhome(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        items = Item.objects.filter(item_name__icontains=search)
        result = {}
        for item in items:
            shop = item.shop_id
            print(item)
            print(shop)
            shop_info = Shop.objects.get(pk = shop)
            # result[shop_id] = shop_info
        print(result)
        return HttpResponse(items)
    return render(request, 'userhome.html')