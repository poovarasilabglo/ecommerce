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
           
           
    

    ]
