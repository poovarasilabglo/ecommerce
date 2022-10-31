from django.db import models
from django.contrib.auth.models import User


SUCCESS = 1
PENDING = 2
FAILED = 3
ORDER_STATUS_CHOICES = (
        (SUCCESS, 'Success'),
        (PENDING, 'Pending'),
        (FAILED, 'Failed')
)

    
class TimeStampedModel(models.Model):
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     class Meta:
         abstract = True

class category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class products(TimeStampedModel):  
    Category = models.ForeignKey(category, on_delete=models.CASCADE)
    name_of_product = models.CharField(max_length=60) 
    price = models.IntegerField(default=0)
    brand = models.CharField(max_length=60)
    img = models.ImageField(upload_to = "images/")
    in_stock = models.BooleanField(default = True)
    
    def __str__(self):
        return '{}'.format(self.name_of_product)
    
class Cart(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    is_active = models.BooleanField(default = False)
    def __str__(self):
        return '{} {}'.format(self.products,self.user)
        
        
    def get_total_products_price(self):
        return self.quantity * self.price 
          
        
class order(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_name = models.ManyToManyField(Cart)
    order_status = models.IntegerField(default= 2,choices = ORDER_STATUS_CHOICES) 
    status = models.BooleanField(default = False)
 


class Wishlist(TimeStampedModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(products, on_delete = models.CASCADE)
   
