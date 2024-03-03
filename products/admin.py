from django.contrib import admin

from products.models import Product, SKU

class SKUInline(admin.TabularInline):
    model = SKU
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "managed_by","edited_at","ingredients" )
    ordering = ("-id",)
    search_fields = ("name",)
    list_filter = ("is_refrigerated", "category")
    fields = (
        ("name"),
        ("category", "is_refrigerated"),
        "description",
        ("id", "created_at"),
        "managed_by",
    )
    autocomplete_fields = ("category", "managed_by")
    readonly_fields = ("id", "created_at")
    inlines = [SKUInline]


class ProductInline(admin.StackedInline):
    """
    For display in CategoryAdmin
    """

    model = Product
    extra = 0
    ordering = ("-id",)
    readonly_fields = ("name", "is_refrigerated")
    fields = (readonly_fields,)
    show_change_link = True


@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'cost_price', 'platform_commission', 'selling_price','status')
    list_filter = ('status',) 
    search_fields = ('product__name', 'size')
    autocomplete_fields = ['product'] 