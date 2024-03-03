from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
)
from django.http import JsonResponse
from .models import Product, Status, SKU
from .serializers import ProductListSerializer, SKUSerializer
from django.utils import timezone


@api_view(["GET","POST","PATCH"])
@permission_classes([AllowAny])
def products_list(request):
    if request.method == 'GET':
        """
        List of all products.
        """
        refrigerated_param = request.query_params.get('is_refrigerated')
        if refrigerated_param:
            if refrigerated_param.lower() == 'true':
                products = Product.objects.filter(is_refrigerated=True)
            elif refrigerated_param.lower() == 'false':
                products = Product.objects.filter(is_refrigerated=False)
            else:
                return Response({"error": "Invalid value for refrigerated parameter. Valid values are 'true' or 'false'."}, 
                                status=HTTP_400_BAD_REQUEST)
        else:
            products = Product.objects.all()

        serializer = ProductListSerializer(products, many=True)
        return Response({"products": serializer.data}, status=HTTP_200_OK)
    
    if request.method == 'POST':
        try:
            serializer = ProductListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Product is Added'}, status=HTTP_201_CREATED)
            return Response({'error msg':serializer.errors},status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error msg':str(e)})
        
    if request.method == 'PATCH':
        try:
            product_name = request.data.get('name',None)
            product = Product.objects.get(name=product_name)
            serializer = ProductListSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                product.edited_at = timezone.now()
                serializer.save()
                return Response({'msg':'Product is Updated'},status=HTTP_201_CREATED)
            return Response({'error msg':serializer.errors}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error msg':str(e)}, status=HTTP_400_BAD_REQUEST)
        

@api_view(["POST"])
@permission_classes([AllowAny])
def sku_create_view(request):
    if request.method == "POST":
        # Set the default status for a new SKU
        request.data["status"] = Status.PENDING  # Set to Pending for approval
        # Create a serializer instance with the data provided in the request
        serializer = SKUSerializer(data=request.data)
        # Validate the serializer data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def product_detail(request, product_id):
    try:
        # Retrieve the product object
        product = Product.objects.get(id=product_id)
        
        # Serialize the product object along with its related SKUs
        serializer = ProductListSerializer(product)
        
        # Return the serialized data
        return Response(serializer.data, status=HTTP_200_OK)
    except Product.DoesNotExist:
        # Handle the case when the product does not exist
        return Response({"error": "Product not found"}, status=HTTP_404_NOT_FOUND)
    

@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def edit_sku_status(request, sku_id):
    try:
        sku = SKU.objects.get(id=sku_id)
        # Check if the user has permission to edit SKUs
        if not request.user.has_perm('yourapp.change_sku'):
            return Response({"error": "You do not have permission to edit SKU"}, status=HTTP_403_FORBIDDEN)
        # Update the status based on the request data
        sku.status = request.data.get('status', sku.status)
        sku.save()

        serializer = SKUSerializer(sku)
        return Response(serializer.data, status=HTTP_200_OK)
    except SKU.DoesNotExist:
        return Response({"error": "SKU not found"}, status=HTTP_404_NOT_FOUND)
    

def all_skus_with_category(request):
    skus_with_category = SKU.objects.select_related('category').all()
    skus_data = [{'name': sku.name, 'category': sku.category.name} for sku in skus_with_category]
    return JsonResponse(skus_data, safe=False)
