from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product
from .Serializer import CustomerSerializer, ProductSerializer
from rest_framework.decorators import api_view, permission_classes,authentication_classes
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
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import jwt
from datetime import datetime, timedelta
import json
from django.contrib.auth.tokens import default_token_generator
from urllib.parse import parse_qs, urlparse







# Create your views here.
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def about(req):
    return Response("about")


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


class MyAuthView(APIView):
    """
    This class handles the AUTH operations for MyModel
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

            # Check if any of the fields are empty
            if not all([first_name, last_name, email, address, city, password]):
                return Response({"message": "All fields are required"})

            # Checking if the email already exists
            if Customer.objects.filter(email=email).exists():
                return Response({"message": "Email is already in use"})

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

        
    @api_view(['GET'])
    def emailCheckForRegister(request):
        email = request.data.get('email')  # Use request.data to access the POST data
        try:
            user = Customer.objects.get(email=email)  # Check if a user with the given email exists
            return Response('Email is already in use', status=401)
        except Customer.DoesNotExist:
            return Response("Email isn't in use", status=200)


    @api_view(['POST'])
    def login_view(request):
        if request.method == 'POST':
            data = request.data

            email = data.get('email')
            password = data.get('password')
            try:
                customer = Customer.objects.get(email=email)

                if check_password(password, customer.password):
                    # Generate the token
                    payload = {
                        'customerID': customer.customerID,  # Include customerID in the payload
                        'email': customer.email,
                        'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time
                    }
                    token = jwt.encode(payload, 'secret_key', algorithm='HS256')  # Use your own secret key

                    # Return the token and customerID
                    return Response({"token": token, "customerID": customer.customerID})
                else:
                    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            except Customer.DoesNotExist:
                return Response({"error": "Invalid credentials"})
        else:
            return Response("Invalid request method", status=status.HTTP_400_BAD_REQUEST)



@permission_classes([IsAuthenticated])
class MyCustomerView(APIView):
    """
    This class handles the Customer operations for MyModel
    """
    
    def getCustomer(self, request, customer_id):
        # Retrieve the customer from the database
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return Response({'message': 'Customer not found'}, status=404)

        # Return the customer's data
        data = {
            'customerID': customer.customerID,
            'firstName': customer.firstName,
            'lastName': customer.lastName,
            'email': customer.email,
            'address': customer.address,
            'city': customer.city,
        }
        return Response(data)
    
    
    @api_view(['PATCH'])
    def changeDetails(request):
        authorization_header = json.loads(request.body)["Authorization"]
        custoerChanges = json.loads(request.body)["userChanges"]
  
        if not authorization_header or 'Bearer ' not in authorization_header:
            return Response({"error": "Invalid authorization header"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Extract the token from the header
            token = authorization_header.split(' ')[1]
            
            # Decode the token and retrieve the customerID
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
            customerID = payload['customerID']
            
        except (jwt.exceptions.DecodeError, IndexError, KeyError):
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(customerID=customerID)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        # Update the fields based on the provided data
        if  custoerChanges['profileData']['firstName'] != '': #need to change user to changeUser fields
            customer.firstName = custoerChanges['profileData']['firstName']
        if custoerChanges['profileData']['lastName'] != '':
            customer.lastName = custoerChanges['profileData']['lastName']
        if custoerChanges['profileData']['email'] != '':
            customer.email = custoerChanges['profileData']['email']
        if custoerChanges['profileData']['address'] != '':
            customer.address = custoerChanges['profileData']['address']
        if custoerChanges['profileData']['city'] != '':
            customer.city = custoerChanges['profileData']['city']
        # Need to update password too but i need to figure out how do i incrypet in when udating!!!!!!!!

        # Save the changes
        customer.save()

        # Return the updated customer's data
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    




@api_view(['POST'])
def lostPassword(request):
    # Check if the cusemail exists in the Customer table
    try:
        customer = Customer.objects.get(email=json.loads(request.body)["email"])
    except Customer.DoesNotExist:
        return Response({'message': 'Customer not found'}, status=404)
    
    # Generate a token
    token = default_token_generator.make_token(customer) # NEED TO FIND A WAY TO MAKE THE TOKEN LAST 10 MINS
    
    # Update the customer's token field
    customer.token = token
    customer.save()

    # Return the customer's data
    data = {
        'email': customer.email,
        'token': token,
    }
    print(data)
    return Response(data)


@api_view(['POST'])
def resetPassword(request):
    url = request.data.get('url')
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    token = query_params.get('token', [None])[0]
    try:
        customer = Customer.objects.get(token=token)  # Find the user associated with the token
        
    except Customer.DoesNotExist:
        return Response('Invalid token', status=400)
    new_password = request.data.get('password')  # Get the new password from the request
    
    # Verify the token and change the password
    
    customer.password = make_password(new_password)
    customer.token = ''
    customer.save()
    return Response('Password reset successfully', status=200)
    
  

   