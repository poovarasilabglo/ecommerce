from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from app.form import RegisterForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View,TemplateView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q,F
from django.db.models import Sum
from app.models import *
from django.core import serializers
#from django.http import JsonResponse


# login page
class user_login(View):
    template_name = 'login.html'
    success_url ='/read'    


# Register page
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in {username}')
            return redirect('accounts/login')
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})



# logout page
class user_logout(View):
    def get(self, request):
        logout(request)
        return redirect('/accounts/logout/')


# product create page
class products_create(CreateView):
    model = products
    fields = '__all__'
    template_name = 'create.html'
    
    
# all product view page 
class products_read(LoginRequiredMixin,  ListView):
    model = products
    template_name = 'read.html'
    success_url ='/read'
    
    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter( Q(name_of_product__icontains=query) | Q(brand__icontains=query) )
        #print(qs)
        return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        l = []
        wish = list(Wishlist.objects.filter(user = self.request.user).values('product__id'))
        for i in wish:
            for j, k in i.items():
                l.append(k)
        #print(l)
        context['wish_product'] =l
        #print(context)
        return context 
              
        
        
#productlist display in json format    
class productsview_json(ListView):
    model = products  
    def get(self,request, *args, **kwargs):
        qs = products.objects.all()
        qs_json = serializers.serialize('json', qs, indent =4)
        print(type(qs_json))
        return HttpResponse(qs_json, content_type='application/json')


# add to cart page
class Add_Cart(LoginRequiredMixin,TemplateView):
    template_name = 'mycart.html'
    success_url ='read'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['id']
        product_obj = products.objects.get(id=product_id)
        context['cart_obj'] = Cart.objects.create(user = self.request.user, products = product_obj, quantity =1, price = product_obj.price)
        return context 
              

# add to quantity
def Add_qua(request,id):
    cart_obj = Cart.objects.get(id = id)
    cart_obj.quantity = request.GET.get('quantity')
    cart_obj.save()
    return redirect('cartlist')


# card page listview
@login_required(redirect_field_name='/cartlist', login_url='/apps')
def show_cart(request):
    cart_obj = Cart.objects.filter(is_active = False)
    return render (request, 'add_card.html', {'cart_obj': cart_obj})



#cartlist display json format
class cart_json(ListView):
    model = Cart 
    def render_to_response(self, context, **kwargs):
        qs = Cart.objects.filter(is_active = False)
        #print(qs)
        qs_json = serializers.serialize('json', qs, indent =4)
        #print(type(qs_json))
        return HttpResponse(qs_json, content_type='application/json')

 

#remove to product in cart
def Remove_cart(request,id):
    if request.method == "POST":
        cart_remove = Cart.objects.get(id=id)
        cart_remove.delete()
        return redirect('cartlist')


#order views 
@login_required   
def order_view(request):
    if request.method == "POST":
        carts = Cart.objects.filter(Q(user = request.user) & Q(is_active = False))
        created = order.objects.create(user = request.user) 
        created.product_name.add(*carts)
        carts.update(is_active = True)
        orders_product = order.objects.latest('product_name__id')
        order_obj = orders_product.product_name.all()
        total = order_obj.aggregate(total = Sum(F('price') * F('quantity')))['total']
        tax = total * orders_product.tax
        subtotal = total + tax
        context = {
            'orders_product':orders_product,
            'order_obj':order_obj,
            'Tax':tax,
            'total':subtotal
        }  
        return render(request, 'order_summary.html', context)
    else:
        return HttpResponse("your not checkout products")
  

   
#order history view 
def order_show(request):
    if request.method == "GET":
        orders_product = order.objects.latest('product_name__id')
        order_obj = orders_product.product_name.filter(cart_status= 2)
        total = order_obj.aggregate(total = Sum(F('price') * F('quantity')))['total']
        tax = total * orders_product.tax
        subtotal = total + tax
        context = {
            'orders_product':orders_product,
            'order_obj':order_obj,
            'Tax':tax,
            'total':subtotal
        }  
        return render(request, 'order_summary.html', context)  
    
 


class order_json(ListView):
    model = order  
    def get(self,request, *args, **kwargs):
        orders_product = order.objects.latest('product_name__id')
        order_obj = orders_product.product_name.filter(cart_status= 2)
        qs_json = serializers.serialize('json', order_obj, indent =4)
        print(type(qs_json))
        return HttpResponse(qs_json, content_type='application/json')

 
 
    
#delete all product in orderpage
def cancel_order(request,id):
    if request.method == "POST":
        order_remove = order.objects.get(id = id)
        order_remove.order_status = 3
        order_remove.save()
        return redirect('order_show')

def Remove_single_order(request,id):
    single_remove = Cart.objects.get(id=id)
    single_remove.cart_status = 3
    single_remove.save()
    return redirect('order')
    
#wishlist add    
def Add_Wishlist(request,id):
    if request.method == "POST":
        product_obj = products.objects.get(id=id)
        wishlist,created = Wishlist.objects.get_or_create(user=request.user, product=product_obj)
        if created:
            messages.info(request,'The item was added to your wishlist')
        else:
            messages.info(request,'The item was already in your wishlist')
    return redirect('read')



#wishlist show page 
@login_required(redirect_field_name='/wish_list', login_url='/accounts/login')  
def wish_list(request):
    wishlist = Wishlist.objects.filter(user = request.user)
    context ={
        'wishlist':wishlist
    }
    return render(request,'wishlist.html',context)


#wishlist remove 
def Remove_wishlist(request,id):
    if request.method == "POST":
        wish_remove = Wishlist.objects.get(id = id)
        wish_remove.delete()
        return redirect('wish_list')


#wishlist display json format
class wishlist_json(ListView):
    model = Wishlist 
    def render_to_response(self, context, **kwargs):
        qs = Wishlist.objects.all()
        print(qs)
        qs_json = serializers.serialize('json', qs, indent =4)
        print(type(qs_json))
        return HttpResponse(qs_json, content_type='application/json')

 
 
 #total order history
def My_order_allhistory(request):
     orders = order.objects.filter(user = request.user)
     return render (request, 'my_order.html', {'orders': orders})



  
  
  
  
  
  
  
  
  
  
  

  
  
  
 
       
