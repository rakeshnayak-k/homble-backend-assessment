from django.core.management.base import BaseCommand
from ...products.models import SKU

class Command(BaseCommand):
    help = 'Automatically update the price fields for existing SKU records'

    def handle(self, *args, **options):
        # Update price fields for existing SKU records
        skus = SKU.objects.all()
        for sku in skus:
            selling_price = sku.selling_price
            platform_commission = selling_price * 0.25  # 25% of selling_price
            cost_price = selling_price - platform_commission
            sku.platform_commission = platform_commission
            sku.cost_price = cost_price
            sku.save()

        self.stdout.write(self.style.SUCCESS('Price fields updated successfully'))
