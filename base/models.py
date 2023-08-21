from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission


class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        email = self.normalize_email(email)
        customer = self.model(email=email, **extra_fields)
        customer.set_password(password)
        customer.save()
        return customer

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    customerID = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50, null=True, blank=True)
    lastName = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    image = models.ImageField(blank=True, null=True,upload_to="images")
    last_login = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=255, blank=True, null=True)


    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def get_email_field_name(self):
        return 'email'

    def __str__(self):
        return self.firstName

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    # Custom related_name for groups field
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this customer belongs to.',
        related_name='customer_set',  # Custom related_name
        related_query_name='customer'
    )

    # Custom related_name for user_permissions field
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this customer.',
        related_name='customer_set',  # Custom related_name
        related_query_name='customer'
    )

class Categories(models.Model):
    category=models.CharField(max_length=30,null=True,blank=True)
    category_image = models.ImageField(blank=True, null=True)


    fields =[category]
 
    def __str__(self):
           return self.category

class Product(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    createdTime=models.DateTimeField(auto_now_add=True)
    season=models.CharField(max_length=50,null=True,blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True)
    image=models.ImageField( blank=True,null=True,upload_to="images") 
    description= models.CharField(max_length=300,null=True,blank=True)
    reviews = models.TextField(blank=True, null=True)
    fields =['name','price','image','category']


    def set_reviews(self, data):
        self.reviews = json.dumps(data)

    def get_reviwes(self):
        return json.loads(self.reviews) if self.reviews else []
 
    def __str__(self):
           return self.name
    
    @property
    def category_name(self):
        return self.category.category
    
from django.db import models
import json

class Purchases(models.Model):
    purchaseID = models.AutoField(primary_key=True)
    user_ID = models.TextField(null=False)
    purchase_date = models.DateTimeField(auto_now_add=True)
    OrderSummary = models.TextField(blank=True, null=True)
    DeliveryDetails = models.TextField(blank=True, null=True)

    fields = ['purchaseID']

    def set_order_summary(self, data):
        self.OrderSummary = json.dumps(data)

    def get_order_summary(self):
        return json.loads(self.OrderSummary) if self.OrderSummary else []

    def set_delivery_details(self, data):
        self.DeliveryDetails = json.dumps(data)

    def get_delivery_details(self):
        return json.loads(self.DeliveryDetails) if self.DeliveryDetails else []

    def __str__(self):
        return str(self.purchaseID)

    

class Reviews(models.Model):
    product_ID=models.DecimalField(max_digits=100,decimal_places=0)
    user_ID=models.DecimalField(max_digits=100,decimal_places=0)
    text=models.CharField(max_length=1200,null=True,blank=True)
    List_of_product_ID=models # i didnt finish this field

    fields =['product_ID']
 
    def __str__(self):
           return self.product_ID
    


