from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .serializers import CategorySerializer
from .permission import IsAdminOrStaff
from django.http import JsonResponse


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrStaff])
def category_list_with_products(request):
    categories = Category.objects.prefetch_related('products').all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


def active_categories_with_sku_count(request):
    active_categories = Category.objects.filter(is_active=True).prefetch_related('skus')
    categories_data = [{'name': category.name, 'sku_count': category.skus.filter(status='approved').count()} for category in active_categories]
    return JsonResponse(categories_data, safe=False)
