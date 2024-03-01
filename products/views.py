from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
)

from .models import Product
from .serializers import ProductListSerializer
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
        
