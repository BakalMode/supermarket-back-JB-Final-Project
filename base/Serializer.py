from rest_framework import serializers
from .models import Categories, Product,Customer, Purchases



from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['category']


class PurchesesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = '__all__'