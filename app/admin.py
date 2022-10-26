from django.contrib import admin
from app.models import category
from app.models import products
from app.models import Cart
from app.models import order

class categoryadmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(category,categoryadmin) 

class productsadmin(admin.ModelAdmin):
    list_display = ('id','Category','name_of_product','price','brand','img',)

admin.site.register(products,productsadmin) 

class Cartadmin(admin.ModelAdmin):
    list_display = ('user','products','quantity','price',)

admin.site.register(Cart,Cartadmin)   


class orderadmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(order,orderadmin)   
