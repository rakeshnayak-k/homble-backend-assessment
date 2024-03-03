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
    markup_percentage = serializers.SerializerMethodField()

    class Meta:
        model = SKU
        fields = "__all__"

    def get_markup_percentage(self, obj):
        if obj.cost_price != 0:
            return obj.platform_commission / obj.cost_price * 100
        return 0 