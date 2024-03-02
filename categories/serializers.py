from rest_framework import serializers
from .models import Category
from products.serializers import ProductListSerializer

class CategorySerializer(serializers.ModelSerializer):
    count_products = serializers.IntegerField(source='product_count')  # Assume the property name is 'product_count'
    products = ProductListSerializer(many=True, read_only=True)  # Nested serializer to list all products

    class Meta:
        model = Category
        fields = ['id', 'name', 'is_active', 'count_products', 'products']
