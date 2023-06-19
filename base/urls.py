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
    # path('editprofile/<int:customer_id>', views.MyCustomerView.as_view()),
    path('forgotpassword', views.lostPassword),
    path('resetpassword', views.resetPassword),
    path('emailcheckforregister', views.MyAuthView.emailCheckForRegister),
]
