from django.urls import path,include
from app.views import * 
from app import views

urlpatterns = [
           
           path('login/',user_login.as_view(),name = 'login'),
           path("register/",views.register, name="register"),
           path('logout/',user_logout.as_view(),name = 'logout'),
           path('create/',products_create.as_view(),name = 'create'),
           path('read/',products_read.as_view(),name = 'read'),
           path("accounts/", include("django.contrib.auth.urls")),
           path('addcart/<int:id>',Add_Cart.as_view(),name = 'addcart'),
           path('qua/<int:id>',views.Add_qua,name = 'qua'),
           path('cartlist/',views.show_cart,name = 'cartlist'),
           path('remove/<int:id>',views.Remove_cart,name = 'remove'),
           path('order/',views.order_view,name = 'order'),
           path('order_show/',views.order_show,name = 'order_show'),
           path('order_remove/<int:id>',views.cancel_order,name = 'order_remove'),
           path('remove_single/<int:id>',views.Remove_single_order,name = 'remove_single'),
           path('wishlist/<int:id>',views.Add_Wishlist,name = 'wishlist'),
           path('wish_list/',views.wish_list,name = 'wish_list'),
           path('remove_wish/<int:id>',views.Remove_wishlist,name = 'remove_wish'),
           path('myorder/',views.My_order_allhistory,name = 'myorder'),
           path('js/',productsview_json.as_view(), name='js'),
           path('order_js/',order_json.as_view(), name='order_js'),
           path('cart_js/',cart_json.as_view(), name='cart_js'),
           path('wish_js/',wishlist_json.as_view(), name='wish_js'),
           path('search_js/',search_product_json.as_view(), name='search_js'),
           #path('charge/',views.charge,name ='charge'),
           path('checkout/',views.create_checkout_sessionview, name = 'checkout'),
           path('success/',Successview.as_view(),name = 'success'),
           path('cancel/',Cancelview.as_view,name = 'cancel'),
           path('webhook/',views.webhook_endpoint,name = 'webhook'),
    ]


