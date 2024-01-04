# myapp/urls.py

from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('loginshop/',views.loginshop , name = 'loginshop'),
    path('signupshop/',views.signupshop , name = 'signupshop'),
    path('logoutshop/',views.logoutshop , name = 'logoutshop'),
    path('addshopdata/',views.AddShopData,name ='AddShopData'),
    path('additem/',views.Additem,name ='Additem'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
