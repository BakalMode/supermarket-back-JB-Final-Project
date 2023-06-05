from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product
from .Serializer import ProductSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .Serializer import ProductSerializer


# Create your views here.
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def about(req):
    return Response("about")

@api_view(['GET'])
def contact(req):
    return Response("contact")

# @permission_classes([IsAuthenticated])
class MyModelView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request):
        """
        Handle GET requests to return a list of MyModel objects
        """
        my_model = Product.objects.all()
        serializer = ProductSerializer(my_model, many=True)
        return Response(serializer.data)


def index(req):
    return print('hello', safe=False)