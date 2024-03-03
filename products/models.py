from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import Permission



class Product(models.Model):
    """
    Very basic structure. To be further built up.
    """
    name = models.CharField(
        _("display name"),
        max_length=150,
        unique=True,
        help_text=_("This will be displayed to user as-is"),
    )
    description = models.TextField(
        _("descriptive write-up"),
        unique=False,
        help_text=_("Few sentences that showcase the appeal of the product"),
    )
    is_refrigerated = models.BooleanField(
        help_text=_("Whether the product needs to be refrigerated"),
        default=False,
    )
    category = models.ForeignKey(
        "categories.Category",
        related_name="products",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    managed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="managed_products",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
        )
    edited_at = models.DateTimeField(
        blank=True,
        null=True,
        )
    ingredients = models.CharField(
        blank=True,
        null=True,
        max_length=500,
        )
    

    def save(self, *args, **kwargs):
        self.name = self.name.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name})"

    class Meta:
        # Just to be explicit.
        db_table = "product"
        ordering = []
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Status(models.IntegerChoices):
    PENDING = 1, _('Pending for approval')
    APPROVED = 2, _('Approved')
    DISCONTINUED = 3, _('Discontinued')

class SKU(models.Model):
    # Define choices for measurement units
    GM = 'gm'
    KG = 'kg'
    ML = 'mL'
    L = 'L'
    PC = 'pc'
    MEASUREMENT_UNIT_CHOICES = [
        (GM, 'Gram'),
        (KG, 'Kilogram'),
        (ML, 'Milliliter'),
        (L, 'Liter'),
        (PC, 'Piece'),
    ]
    status = models.IntegerField(
        _("status"),
        choices=Status.choices,
        default=Status.PENDING,  # Default to Pending for approval
        help_text=_("Status of the SKU")
    )


    product = models.ForeignKey(
        "Product",
        related_name="skus",
        on_delete=models.CASCADE
    )
    size = models.CharField(
        _("size"),
        max_length=150,
        validators=[MaxValueValidator(999)],
        help_text=_("Size of the product, e.g., 200 gm, 500 gm, etc.")
    )
    measurement_unit = models.CharField(
        _("measurement unit"),
        max_length=2,
        choices=MEASUREMENT_UNIT_CHOICES,
        default=PC,  # Default to piece
        help_text=_("Measurement unit of the product")
    )
    selling_price = models.PositiveSmallIntegerField(
        _("selling price (Rs.)"),
        help_text=_("Price payable by customer (Rs.)"),
    )
    platform_commission = models.PositiveSmallIntegerField(
        _("platform commission"),
        help_text=_("Commission charged by the platform (Rs.)"),
        null=True,
    )
    cost_price = models.PositiveSmallIntegerField(
        _("cost price (Rs.)"),
        help_text=_("Cost price of the product (Rs.)"),
        null=True,
    )
    # edit_sku_permission = Permission.objects.create(
    # codename='edit_sku',
    # name='Can edit SKU status',
    # )
    def save(self, *args, **kwargs):
        # Set selling_price as the sum of cost_price and platform_commission
        self.selling_price = self.cost_price + self.platform_commission
        super().save(*args, **kwargs)

    def get_status_display_text(self):
        return dict(Status.choices)[self.status]
    
    def __str__(self):
        return f"{self.product.name} - {self.size} ({self.get_measurement_unit_display()} - Rs. {self.selling_price}) - {self.get_status_display_text()}"

    class Meta:
        db_table = "sku"
        ordering = []
        verbose_name = "SKU"
        verbose_name_plural = "SKUs"


