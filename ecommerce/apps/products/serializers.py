from rest_framework import serializers
from .models import (
    Brand,
    Category,
    Product,
    ProductImage,
    ProductVariant,
    ProductAttribute,
)


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'is_active',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'slug',
            'created_at',
        ]


class CategorySerializer(serializers.ModelSerializer):

    parent_name = serializers.CharField(
        source='parent.name',
        read_only=True
    )

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'parent',
            'parent_name',
            'is_active',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'slug',
            'parent_name',
            'created_at',
        ]


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = [
            'id',
            'product',
            'image',
            'alt_text',
            'is_primary',
            'display_order',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]


class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'product',
            'name',
            'sku',
            'price',
            'stock',
            'is_active',
        ]

        read_only_fields = [
            'id',
        ]


class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = [
            'id',
            'product',
            'name',
            'value',
        ]

        read_only_fields = [
            'id',
        ]


class ProductSerializer(serializers.ModelSerializer):

    brand_name = serializers.CharField(
        source='brand.name',
        read_only=True
    )

    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    variants = ProductVariantSerializer(
        many=True,
        read_only=True
    )

    attributes = ProductAttributeSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'sku',
            'brand',
            'brand_name',
            'category',
            'category_name',
            'description',
            'price',
            'discount_price',
            'stock',
            'status',
            'is_featured',
            'is_active',
            'images',
            'variants',
            'attributes',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'slug',
            'brand_name',
            'category_name',
            'images',
            'variants',
            'attributes',
            'created_at',
            'updated_at',
        ]
