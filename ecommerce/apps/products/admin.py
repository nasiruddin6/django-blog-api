from django.contrib import admin
from .models import (
    Brand,
    Category,
    Product,
    ProductImage,
    ProductVariant,
    ProductAttribute,
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'slug',
        'is_active',
        'created_at',
    ]

    list_filter = [
        'is_active',
        'created_at',
    ]

    search_fields = [
        'name',
        'slug',
    ]

    readonly_fields = [
        'slug',
        'created_at',
    ]

    ordering = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'slug',
        'parent',
        'is_active',
        'created_at',
    ]

    list_filter = [
        'is_active',
        'created_at',
    ]

    search_fields = [
        'name',
        'slug',
    ]

    autocomplete_fields = [
        'parent',
    ]

    readonly_fields = [
        'slug',
        'created_at',
    ]

    ordering = ['name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'sku',
        'brand',
        'category',
        'price',
        'stock',
        'status',
        'is_featured',
        'is_active',
    ]

    list_filter = [
        'status',
        'is_featured',
        'is_active',
        'brand',
        'category',
    ]

    search_fields = [
        'name',
        'slug',
        'sku',
        'brand__name',
        'category__name',
    ]

    autocomplete_fields = [
        'brand',
        'category',
    ]

    readonly_fields = [
        'slug',
        'created_at',
        'updated_at',
    ]

    inlines = [
        ProductImageInline,
        ProductVariantInline,
        ProductAttributeInline,
    ]

    ordering = ['-created_at']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'alt_text',
        'is_primary',
        'display_order',
        'created_at',
    ]

    list_filter = [
        'is_primary',
        'created_at',
    ]

    search_fields = [
        'product__name',
        'alt_text',
    ]

    autocomplete_fields = [
        'product',
    ]

    readonly_fields = [
        'created_at',
    ]

    ordering = ['display_order']


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'name',
        'sku',
        'price',
        'stock',
        'is_active',
    ]

    list_filter = [
        'is_active',
    ]

    search_fields = [
        'product__name',
        'name',
        'sku',
    ]

    autocomplete_fields = [
        'product',
    ]

    ordering = ['product__name']


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'name',
        'value',
    ]

    search_fields = [
        'product__name',
        'name',
        'value',
    ]

    autocomplete_fields = [
        'product',
    ]

    ordering = ['product__name']
