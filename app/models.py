from django.db import models
from django.contrib.auth.models import User

class category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class products(models.Model):  
    Category = models.ForeignKey(category, on_delete=models.CASCADE, null = True)
    name_of_product = models.CharField(max_length=60) 
    price = models.IntegerField(default=0)
    brand = models.CharField(max_length=60)
    img = models.ImageField(upload_to = "images/",null = True)
    in_stock = models.BooleanField(default = True)
    
    def __str__(self):
        return '{} {}'.format(self.name_of_product,self.id)
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add = True,null = True)
    price = models.FloatField(default=0)
    is_active = models.BooleanField(default = False)
    def __str__(self):
        return '{} {}'.format(self.products,self.user)
        
        
    def get_total_products_price(self):
        return self.quantity * self.price 
          
        
class order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_name = models.ManyToManyField(Cart)
    tax = models.FloatField()
    status = models.BooleanField(default = False)
    
   
