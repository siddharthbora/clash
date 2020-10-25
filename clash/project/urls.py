from django.urls import path
from . import views


urlpatterns = [
    path('',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('success/',views.success,name='success'),
    path('logout/',views.userlogout,name='logout'),
    path('result/', views.success, name='result'),
    path('getrequest/',views.check,name='check'),
    path('emglogin/',views.emglogin,name='emglogin'),
    path('spincheck/',views.checkspin, name='spincheck'),
    path('getassured/',views.getassured,name='getassured')

]