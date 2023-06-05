from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from  . import views


from . import views
urlpatterns = [
    path('', views.index),
    path("products", views.MyModelView.as_view()),
    path("products/<pk>", views.MyModelView.as_view()),
]
