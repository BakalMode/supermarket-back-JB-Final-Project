from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    createdTime=models.DateTimeField(auto_now_add=True)
    season=models.CharField(max_length=50,null=True,blank=True)
    category=models.CharField(max_length=50,null=True,blank=True)
    image=models.ImageField( blank=True,null=True) 

    fields =['name','price','image']
 
    def __str__(self):
           return self.name
    
class Purchases(models.Model):
    order_ID=models.DecimalField(max_digits=100,decimal_places=0)
    user_ID=models.DecimalField(max_digits=100,decimal_places=0)
    purchase_date=models.DateTimeField(auto_now_add=True) 
    List_of_product_ID=models # i didnt finish this field


    fields =[]
 
    def __str__(self):
           return self.order_ID
    

class Reviews(models.Model):
    product_ID=models.DecimalField(max_digits=100,decimal_places=0)
    user_ID=models.DecimalField(max_digits=100,decimal_places=0)
    text=models.CharField(max_length=1200,null=True,blank=True)
    List_of_product_ID=models # i didnt finish this field
    stars=models.DecimalField(max_digits=1,decimal_places=0)



    fields =[]
 
    def __str__(self):
           return self.user_ID
    

class Categories(models.Model):
    category=models.CharField(max_length=30,null=True,blank=True)



    fields =[]
 
    def __str__(self):
           return self.category