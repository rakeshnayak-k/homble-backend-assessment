from django.contrib import admin

from categories.models import Category
from products.admin import ProductInline


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active","count_products")
    ordering = ("id",)
    search_fields = ("name",)
    list_filter = ("is_active",)
    fields = ("id", "name", "is_active","count_products")
    # autocomplete_fields = ()
    readonly_fields = ("id","count_products")
    inlines = (ProductInline,)
