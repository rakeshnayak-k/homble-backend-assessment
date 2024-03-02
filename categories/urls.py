from django.urls import path
from .views import category_list_with_products

urlpatterns = [
    path('categories/', category_list_with_products, name='category-list-with-products'),
]