"""একবার run করলে প্রতিটি model-এর একটি example পাবে।"""
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.products.models import Brand, Category, Product, ProductImage, ProductVariant, ProductAttribute


class Command(BaseCommand):
    help = 'Create one example per model; repeated runs preserve existing practice data.'

    @transaction.atomic
    def handle(self, *args, **options):
        brand, _ = Brand.objects.get_or_create(name='Practice Brand')
        category, _ = Category.objects.get_or_create(slug='practice-category', defaults={'name': 'Practice Category'})
        product, _ = Product.objects.get_or_create(sku='PRACTICE-001', defaults={
            'name': 'Practice T-Shirt', 'brand': brand, 'category': category,
            'price': '500.00', 'discount_price': '450.00', 'stock': 10,
            'status': 'published',
        })
        ProductVariant.objects.get_or_create(sku='PRACTICE-001-M', defaults={
            'product': product, 'name': 'Medium', 'price': '500.00', 'stock': 5,
        })
        ProductAttribute.objects.get_or_create(product=product, name='Material', defaults={'value': 'Cotton'})
        if not ProductImage.objects.filter(product=product).exists():
            # Tiny GIF placeholder; নিজের photo upload করেও practice করবে।
            gif = bytes.fromhex('47494638396101000100800000000000ffffff21f90401000000002c00000000010001000002024401003b')
            image = ProductImage(product=product, alt_text='Practice placeholder', is_primary=True)
            image.image.save('practice.gif', ContentFile(gif), save=True)
        self.stdout.write(self.style.SUCCESS('Practice examples ready. Open /docs/ or /api/v1/products/'))
