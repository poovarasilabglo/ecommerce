from django.urls import path,include
from app.views import * 
from app import views

urlpatterns = [
           
           path('login/',user_login.as_view(),name = 'login'),
           path('logout/',user_logout.as_view(),name = 'logout'),
           path('create/',productscreate.as_view(),name = 'create'),
           path('read/',productsread.as_view(),name = 'read'),
           path("accounts/", include("django.contrib.auth.urls")),
           path('addcart/<int:id>',Add_Cart.as_view(),name = 'addcart'),
           path('qua/<int:id>',views.Add_qua,name = 'qua'),
           path('cartlist/',views.show_cart,name = 'cartlist'),
           path('remove/<int:id>',views.Remove_cart,name = 'remove'),
           path('order/',views.order_view,name = 'order'),
           path('order_remove/<int:id>',views.Remove_order,name = 'order_remove'),
           path('wishlist/<int:id>',views.Add_Wishlist,name = 'wishlist'),
           path('wish_list/',views.wish_list,name = 'wish_list'),
           path('remove_wish/<int:id>',views.Remove_wishlist,name = 'remove_wish'),
           
           
    

    ]
