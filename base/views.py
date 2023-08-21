from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Purchases
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
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import base64
import os
from django.core.files.storage import default_storage
import ast




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
                return Response({"message": "Email is already in use"}, status=401)

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
    @api_view(['POST'])
    def getCustomer(request):
        authorization_header = json.loads(request.body)["Authorization"]

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

        # Return the customer's data
        data = {
            'customerID': customer.customerID,
            'firstName': customer.firstName,
            'lastName': customer.lastName,
            'email': customer.email,
            'address': customer.address,
            'city': customer.city,
            'image': customer.image.name,
        }
        return Response(data)
    
    

    @api_view(['PATCH'])
    def changeDetails(request):
        authorization_header = json.loads(request.body)["Authorization"]
        customerChanges = json.loads(request.body)["userChanges"]
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
        if customerChanges['profileData']['firstName'] != '':
            customer.firstName = customerChanges['profileData']['firstName']
        if customerChanges['profileData']['lastName'] != '':
            customer.lastName = customerChanges['profileData']['lastName']
        if customerChanges['profileData']['email'] != '':
            customer.email = customerChanges['profileData']['email']
        if customerChanges['profileData']['address'] != '':
            customer.address = customerChanges['profileData']['address']
        if customerChanges['profileData']['city'] != '':
            customer.city = customerChanges['profileData']['city']
        
        if 'selectedImage' in customerChanges['profileData']:
            if customerChanges['profileData']['selectedImage'] != '' and "http://127.0.0.1:8000/images" not in customerChanges['profileData']['selectedImage']:
                image_data = customerChanges['profileData']['selectedImage']
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]

                # Delete the old image if it exists
                if customer.image:
                # Get the path of the old image
                    image_path = customer.image.path
            
                    # Delete the image file from storage
                    if default_storage.exists(image_path):
                        default_storage.delete(image_path)

                # Create a file from the base64 image data
                image = ContentFile(base64.b64decode(imgstr), name=f"image.{ext}")
                customer.image = image
        
        #if the person chose to remove the picture this will happen        
        else:
            if customer.image:
                image_path = customer.image.path
                if default_storage.exists(image_path):
                    default_storage.delete(image_path)
            customer.image = ""
            


        if customerChanges['profileData']['password'] != '':
            # Encode the password using make_password()
            new_password = customerChanges['profileData']['password']
            customer.password = make_password(new_password)
       
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




#this is for diplaying the categories in the navbar
from .models import Categories

@api_view(['GET'])
def menu_view(request):
    categories = Categories.objects.all()
    category_names = [category.category for category in categories]

    return Response(category_names)

@api_view(['POST'])
def get_product_fields(request):
    try:
        id = request.data.get('id')  # Access the ID value from the request data
        product = Product.objects.get(id=id)
        data = {
            'name': product.name,
            'price': str(product.price),
            'season': product.season,
            'category': str(product.category),
            'image': product.image.name if product.image else None,
            'description': product.description,
            'reviews': str(product.reviews) if product.reviews is not None else None,
        }
        return Response({'data': data})
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)



@api_view(['POST'])
def add_purchase(request):
    
    try:
        authorization_header = json.loads(request.body)["Authorization"]
    except (json.JSONDecodeError, KeyError):
        authorization_header = ""

    if not authorization_header or 'Bearer ' not in authorization_header:
        # Set user_ID to formData username
        form_data = json.loads(request.body)['data']['formData']
        customerID = form_data.get('firstName')

        # Check if username is provided in formData
        if not customerID:
            return Response({"error": "Invalid authorization header and missing username"}, status=status.HTTP_400_BAD_REQUEST)
    else:
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

    purchase_date = datetime.now()
    form_data = json.loads(request.body)['data']['formData']
    cart_items = request.data['data']['cartItems']

    if not authorization_header or 'Bearer ' not in authorization_header:
        purchase = Purchases(user_ID=f"guest:{customerID}", purchase_date=purchase_date, OrderSummary=cart_items, DeliveryDetails=form_data)
    else:
        purchase = Purchases(user_ID=customerID, purchase_date=purchase_date, OrderSummary=cart_items, DeliveryDetails=form_data)
    
    purchase.save()

    return Response("Purchase added successfully!")

@api_view(['POST'])
def createReview(request):
    authorization_header = json.loads(request.body)["Authorization"]

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

    review_data = request.data.get('review')  # Get the 'review' part of the data
    product_id = review_data.get('productId')
    review_text = review_data.get('reviewText')

    try:
        product = Product.objects.get(id=product_id)

        if not Purchases.objects.filter(user_ID=customerID).exists():
            return Response({"error": "Customer has not made any purchases"}, status=status.HTTP_403_FORBIDDEN)

        purchase = Purchases.objects.get(user_ID=customerID)
        order_summary = ast.literal_eval(purchase.OrderSummary)

        for item in order_summary:
            if item['product']['id'] == int(product_id):
                # Product ID exists in order_summary
                break
        else:
            # Product ID does not exist in order_summary
            return Response({"error": "Customer has not purchased the product"}, status=status.HTTP_403_FORBIDDEN)



    
        reviews = product.get_reviwes()

        reviews.append(review_text)
        product.set_reviews(reviews)
        product.save()
        return Response({'success': True})
    
    except Product.DoesNotExist:
        return Response({'success': False, 'error': 'Product not found'})
    
    except Exception as e:
        return Response({'success': False, 'error': str(e)})




@api_view(['POST'])
def purchasedBefore(request):
    authorization_header = json.loads(request.body)["Authorization"]

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

    product_id = request.data.get('idd')  # Get the 'review' part of the data

    try:
        product = Product.objects.get(id=product_id)

        # Retrieve all purchases for the customer
        purchases = Purchases.objects.filter(user_ID=customerID)

        if not purchases.exists():
            return Response({"error": "Customer has not made any purchases"})

        for purchase in purchases:
            order_summary = ast.literal_eval(purchase.OrderSummary)
            for item in order_summary:
                if item['product']['id'] == int(product_id):
                    # Product ID exists in order_summary
                    return Response({'data': True}) 

        # Product ID does not exist in any of the orders
        return Response({'data': False})

    except Product.DoesNotExist:
        return Response({'data': False})

    except Exception as e:
        return Response({'data': False})

    

@api_view(['POST']) #this was added so you would'nt be able to just change the cart local storage and mess with the price :)
def calcTotal(request):
    cart = request.data
    total_cost = 0
    for cart_item in cart:
        product_id = cart_item['product']['id']
        quantity = cart_item['quantity']

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': f'Product with id {product_id} does not exist.'}, status=400)

        total_cost += product.price * quantity
    return Response({'total_cost': total_cost})