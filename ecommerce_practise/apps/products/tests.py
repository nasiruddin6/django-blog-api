import tempfile
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import override_settings
from rest_framework.test import APITestCase
from .models import Brand, Category, Product, ProductImage, ProductVariant, ProductAttribute


class PracticeAPITests(APITestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        config = override_settings(MEDIA_ROOT=folder.name)
        config.enable()
        self.addCleanup(config.disable)

    def test_brand_crud(self):
        url = '/api/v1/brands/'
        r = self.client.post(url, {'name': 'Brand'}, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data['slug'], 'brand')
        detail = f"{url}{r.data['id']}/"
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertEqual(self.client.get(detail).status_code, 200)
        self.assertEqual(self.client.post(url, {'name': 'Brand'}).status_code, 400)
        self.assertEqual(self.client.put(detail, {'name': 'Renamed'}, format='json').status_code, 200)
        self.assertEqual(self.client.patch(detail, {'description': 'Edited'}, format='json').status_code, 200)
        self.assertEqual(self.client.delete(detail).status_code, 204)
        self.assertEqual(self.client.get(detail).status_code, 404)

    def test_seed_repeatable(self):
        models = [Brand, Category, Product, ProductImage, ProductVariant, ProductAttribute]
        call_command('seed_practice')
        self.assertEqual([m.objects.count() for m in models], [1]*6)
        Product.objects.update(stock=42)
        call_command('seed_practice')
        self.assertEqual([m.objects.count() for m in models], [1]*6)
        self.assertEqual(Product.objects.get().stock, 42)
        self.assertEqual(self.client.get('/docs/').status_code, 200)

    def test_relations_validation_upload_and_delete(self):
        call_command('seed_practice')
        product = Product.objects.get()
        url = f'/api/v1/products/{product.pk}/'
        for data in [{'price': '-1.00'}, {'discount_price': '600.00'}, {'price': '400.00'}]:
            self.assertEqual(self.client.patch(url, data, format='json').status_code, 400)
        self.assertEqual(self.client.patch(url, {'discount_price': None}, format='json').status_code, 200)
        buffer = BytesIO()
        Image.new('RGB', (2, 2)).save(buffer, format='PNG')
        image = SimpleUploadedFile('shirt.png', buffer.getvalue(), content_type='image/png')
        self.assertEqual(self.client.post('/api/v1/product-images/', {'product': product.pk, 'image': image}, format='multipart').status_code, 201)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['images']), 2)
        self.assertEqual(len(response.data['variants']), 1)
        self.assertEqual(len(response.data['attributes']), 1)
        self.assertEqual(response.data['brand_name'], product.brand.name)
        self.assertEqual(self.client.delete(f'/api/v1/categories/{product.category_id}/').status_code, 400)
        self.assertEqual(self.client.delete(f'/api/v1/brands/{product.brand_id}/').status_code, 204)
        product.refresh_from_db()
        self.assertIsNone(product.brand_id)
        self.assertEqual(self.client.delete(url).status_code, 204)
        for model in [ProductImage, ProductVariant, ProductAttribute]:
            self.assertEqual(model.objects.count(), 0)
        self.assertEqual(self.client.delete(f'/api/v1/categories/{product.category_id}/').status_code, 204)

    def test_category_parent_and_product_creation(self):
        brand = Brand.objects.create(name='Brand')
        parent = Category.objects.create(name='Parent')
        response = self.client.post('/api/v1/categories/', {'name': 'Child', 'parent': parent.pk}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['parent_name'], 'Parent')
        response = self.client.post('/api/v1/products/', {'name': 'Shirt', 'sku': 'S-1', 'brand': brand.pk, 'category': response.data['id'], 'price': '500.00'}, format='json')
        self.assertEqual(response.status_code, 201)
        pk = response.data['id']
        for endpoint, data in [('product-variants', {'name': 'Medium', 'sku': 'S-M', 'price': '500.00'}), ('product-attributes', {'name': 'Material', 'value': 'Cotton'})]:
            response = self.client.post(f'/api/v1/{endpoint}/', {'product': pk, **data}, format='json')
            self.assertEqual(response.status_code, 201)
