from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

class Customer(models.Model):
    customerID = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50,null=True,blank=True)
    lastName = models.CharField(max_length=50,null=True,blank=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    fields = ['firstName', 'lastName', 'customerID']
 
    def __str__(self):
        return self.firstName

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


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