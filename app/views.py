from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from app.models import *
from django.views.generic import View,TemplateView
from django.contrib.auth import login
from django.db.models import Sum



# login page
class user_login(View):
    template_name = 'login.html'
    success_url ='/read'    

# logout page
class user_logout(View):
    def get(self, request):
        logout(request)
        return redirect('/accounts/logout/')


# product create page
class productscreate(CreateView):
    model = products
    fields = '__all__'
    template_name = 'create.html'
    
    
# all product view page 
class productsread(ListView):
    model = products
    template_name = 'read.html'
    success_url ='/read'
    
    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter( Q(name_of_product__icontains=query) | Q(brand__icontains=query) )
        return qs
  


# add to cart page
class Add_Cart(TemplateView):
    template_name = 'mycart.html'
    success_url ='read'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['id']
        product_obj = products.objects.get(id=product_id)
        context['cart_obj'] = Cart.objects.create(user = self.request.user, products = product_obj, price = product_obj.price)
        return context 
              

# add to quantity
def Add_qua(request,id):
    cart_obj = Cart.objects.get(id = id)
    cart_obj.quantity = request.GET.get('quantity')
    cart_obj.save()
    return redirect('read')


# card page listview
@login_required(redirect_field_name='/cartlist', login_url='/apps')
def show_cart(request):
    cart_obj = Cart.objects.filter(is_active = False)
    return render (request, 'add_card.html', {'cart_obj': cart_obj})


#remove to product in cart
def Remove_cart(request,id):
    cart_remove = Cart.objects.get(id=id)
    cart_remove.delete()
    return redirect('cartlist')


#order views    
def order_view(request):
    if request.method == "POST":
        orders = Cart.objects.filter(user = request.user).all()
        orders.update(is_active = True)
        total = 0
        for x in orders:
            quantity = x.quantity
            price =x.price
            tax = 10/100
            subtotal =quantity*price+tax
            print(subtotal)
            total += subtotal
        context = {
            'total':total, 
            'cart':orders
        }    
        #print(total)
        return render(request, 'order_summary.html', context)
    else:
        return HttpResponse("your not checkout products")	
   
 
def Remove_order(request,id):
    order_remove = order.objects.get(id = id)
    order_remove.delete()
    return redirect('order')


#wishlist show page 
@login_required(redirect_field_name='/wish_list', login_url='/accounts/login')  
def wish_list(request):
    wishlist = Wishlist.objects.filter(user = request.user)
    context ={
        'wishlist':wishlist
    }
    return render(request,'wishlist.html',context)


#wishlist add    
def Add_Wishlist(request,id):
    product_obj = products.objects.get(id=id)
    wishlist,created = Wishlist.objects.get_or_create(user=request.user, product=product_obj)
    if created:
        messages.info(request,'The item was added to your wishlist')
    else:
         messages.info(request,'The item was already in your wishlist')
    return redirect('read')


#wishlist remove 
def Remove_wishlist(request,id):
    wish_remove = Wishlist.objects.get(id = id)
    wish_remove.delete()
    return redirect('wish_list')







  
  
  
  
  
  
  
  
  
  
  
  

  
  
  
 
