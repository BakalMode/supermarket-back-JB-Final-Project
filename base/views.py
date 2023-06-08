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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .models import Customer
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token


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
        my_model = Product.objects.all()
        serializer = ProductSerializer(my_model, many=True)
        return Response(serializer.data)


def index(req):
    return print('hello', safe=False)


# Login and Register views
class MyAuthView(APIView):
    """
    This class handle the AUTH operations for MyModel
    """
    @api_view(['POST'])
    def register(request):
        if request.method == 'POST':
            # Get the data from the POST request
            data = request.data

            # Extract the required fields from the data
            first_name = data.get('firstname')
            last_name = data.get('lastname')
            email = data.get('email')
            address = data.get('address')
            city = data.get('city')
            password = data.get('password')

            # Create a new customer object
            customer = Customer(
                firstName=first_name,
                lastName=last_name,
                email=email,
                address=address,
                city=city
            )
            customer.set_password(password)
            customer.save()

            # Return a Response indicating successful registration
            return Response({"message": "Registration successful"})


        else:
            # Return a Response for unsupported request methods
            return Response("Invalid request method", status=400)


    @api_view(['POST'])
    def login_view(request):
        if request.method == 'POST':
            email = request.data.get('email')
            password = request.data.get('password')

            # Check if a user with the provided email exists
            try:
                user = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            # Authenticate the user using the email and password
            user = authenticate(request, email=user.email, password=password)

            if user is not None:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)