from rest_framework import serializers

from products.models import Product, SKU


class ProductListSerializer(serializers.ModelSerializer):
    """
    To show list of products.
    """

    class Meta:
        model = Product
        fields = ["name", "price","edited_at","ingredients"]

class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ['id', 'product', 'size', 'cost_price', 'platform_commission', 'selling_price']
