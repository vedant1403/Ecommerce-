
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('details/<int:pid>',views.details,name='details'),
    path('cart/',views.cart,name='cart'),
    path('Addcart/<int:pid>',views.Addcart,name='Addcart'),
    path('remove/<int:pid>',views.remove,name='remove'),
    path('search/',views.search,name='search'),
    path('range/',views.range,name='range'),
    path('watch/',views.watchList,name='watch'),
    path('laptop/',views.laptopList,name='laptop'),
    path('mobile/',views.mobileList,name='mobile'),
    path('sort/',views.sort,name='sort'),
    path('sort2/',views.sort2,name='sort2'),
    path('updateqty/<int:uval>/<int:pid>',views.updateqty,name='updateqty'),
    path('register',views.register,name='register'),
    path('loginuser',views.loginuser,name='loginuser'),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('vieworder',views.vieworder,name='vieworder'),
    path('payment',views.payment,name='payment'),
    path('insertProduct',views.insertProduct,name='insertProduct'),
]