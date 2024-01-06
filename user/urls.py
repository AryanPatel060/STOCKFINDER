from django.urls import path
from user import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('',views.userhome , name= 'userhome'),
   

]
