from django.shortcuts import render,redirect,HttpResponse
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
def show_cart(request):
    cart_obj = Cart.objects.all()
    return render (request, 'add_card.html', {'cart_obj': cart_obj})

#remove to product in cart
def Remove_cart(request,id):
    cart_remove = Cart.objects.get(id=id)
    cart_remove.delete()
    return redirect('cartlist')

    



      













  
  
  
  
  
  
  
  
  
  
  
  

  
  
  
 
