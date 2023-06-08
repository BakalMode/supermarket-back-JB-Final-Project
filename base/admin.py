from django.contrib import admin

# Register your models here.
from .models import Product,Reviews,Categories,Purchases,Customer


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Reviews)
admin.site.register(Categories)
admin.site.register(Purchases)


