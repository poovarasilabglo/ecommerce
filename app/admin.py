from django.contrib import admin
from app.models import category
from app.models import products
from app.models import Cart
from app.models import order
from app.models import Wishlist
from app.models import payment



class InLineCart(admin.TabularInline):
    model = Cart
    extra = 1
    max_num =3
class InLineWishlist(admin.StackedInline):
    model = Wishlist


class categoryadmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(category,categoryadmin) 

class productsadmin(admin.ModelAdmin):
    inlines = [InLineWishlist, InLineCart]
    list_display = ('id','Category','name_of_product','price','brand','img',)
    search_fields = ('id','name_of_product')
    list_display_links = ('name_of_product','brand')
    list_editable = ('price',)
    list_filter = ('name_of_product','price')
admin.site.register(products,productsadmin) 


class Cartadmin(admin.ModelAdmin):
    search_fields = ('products__name_of_product',)
    list_display = ('user','products','quantity','price','cart_status')

admin.site.register(Cart,Cartadmin)   


class orderadmin(admin.ModelAdmin):
    list_display = ('id','user','created_at','order_status')

admin.site.register(order,orderadmin)


class Wishlistadmin(admin.ModelAdmin):
    list_display = ('user','created_at')

admin.site.register(Wishlist,Wishlistadmin)   


class paymentadmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'email', 'amount', 'paid_status',)

admin.site.register(payment,paymentadmin)   

