from django.urls import path, re_path
from .views import products_list, sku_create_view, product_detail, edit_sku_status

urlpatterns = [
    re_path(r"^$", products_list, name="products-list"),
    path('create_sku/', sku_create_view, name='create_sku'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('sku/<int:sku_id>/edit_status/', edit_sku_status, name='edit_sku_status'),

]
