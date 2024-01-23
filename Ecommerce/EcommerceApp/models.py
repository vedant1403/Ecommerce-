from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

# Create your models here.
class CustomManager(models.Manager):
    def get_price_range(self,r1,r2):
        return self.filter(price__range=(r1,r2))
    
    def Watch_list(self):
        return self.filter(category__exact="watches")
    
    def laptop_list(self):
        return self.filter(category__exact="laptop")
    
    def mobile_list(self):
        return self.filter(category__exact="mobile")
    
    def price_order(self) -> QuerySet:
        return super().get_queryset().order_by("-price")



    

class Product(models.Model):
    wid=models.IntegerField(primary_key=True)
    product_name=models.CharField(max_length=50)
    cat=(('mobile','mobile'),('watches','watches'),('laptop','laptop'))
    category=models.CharField(max_length=50,choices=cat)
    image=models.ImageField(upload_to='pics')
    description=models.CharField(max_length=250)
    price=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=True)
     

    prod=CustomManager()
    objects=models.Manager()



    def __str__(self):
        return self.product_name
class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity= models.PositiveIntegerField(default=0)
    dater_added=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
     

class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    order_id=models.IntegerField()
    quantity= models.PositiveIntegerField(default=0)
    dater_added=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    is_completed=models.BooleanField(default=False)
