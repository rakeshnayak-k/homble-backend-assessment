from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .serializers import CategorySerializer
from .permission import IsAdminOrStaff

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrStaff])
def category_list_with_products(request):
    categories = Category.objects.prefetch_related('products').all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
