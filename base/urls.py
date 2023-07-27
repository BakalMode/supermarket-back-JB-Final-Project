from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from  . import views


from . import views
urlpatterns = [
    path('', views.index),
    path("products", views.MyModelView.as_view()),
    path("products/<pk>", views.MyModelView.as_view()),
    path('register', views.MyAuthView.register),
    path('login', views.MyAuthView.login_view),
    path('editprofile', views.MyCustomerView.changeDetails),
    path('forgotpassword', views.lostPassword),
    path('resetpassword', views.resetPassword),
    path('emailcheckforregister', views.MyAuthView.emailCheckForRegister),
    path('getcustomer', views.MyCustomerView.getCustomer),
    path('menu', views.menu_view),
    path('getproductfields', views.get_product_fields),
    path('addpurchase', views.add_purchase),
    path('createreview', views.createReview),  
    path('purchasedbefore', views.purchasedBefore),
    path('calctotal', views.calcTotal),  
  

]




