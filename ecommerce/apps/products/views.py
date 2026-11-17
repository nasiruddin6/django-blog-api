from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
)
from drf_spectacular.types import OpenApiTypes
from .models import (
    Brand,
    Category,
    Product,
    ProductImage,
    ProductVariant,
    ProductAttribute,
)
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductVariantSerializer,
    ProductAttributeSerializer,
)


# ==================================================
# BRAND API
# ==================================================

@extend_schema(
    tags=['Brand'],
    summary='List and Create Brands',
    description='Retrieve all brands or create a new brand.',
    request=BrandSerializer,
    responses={
        200: BrandSerializer(many=True),
        201: BrandSerializer,
        400: OpenApiResponse(description='Validation error.')
    }
)
@api_view(['GET', 'POST'])
def brand_list_create(request):

    if request.method == 'GET':
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)

    serializer = BrandSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


@extend_schema(
    tags=['Brand'],
    summary='Retrieve, Update and Delete Brand',
    description='Retrieve, update or delete a brand using its ID.',
    parameters=[
        OpenApiParameter(
            name='pk',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='Brand ID'
        )
    ],
    request=BrandSerializer,
    responses={
        200: BrandSerializer,
        204: OpenApiResponse(description='Brand deleted successfully.'),
        400: OpenApiResponse(description='Validation error.'),
        404: OpenApiResponse(description='Brand not found.')
    }
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def brand_detail(request, pk):

    brand = get_object_or_404(Brand, pk=pk)

    if request.method == 'GET':
        serializer = BrandSerializer(brand)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = BrandSerializer(
            brand,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    brand.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ==================================================
# CATEGORY API
# ==================================================

@extend_schema(
    tags=['Category'],
    summary='List and Create Categories',
    description='Retrieve all categories or create a new category.',
    request=CategorySerializer,
    responses={
        200: CategorySerializer(many=True),
        201: CategorySerializer,
        400: OpenApiResponse(description='Validation error.')
    }
)
@api_view(['GET', 'POST'])
def category_list_create(request):

    if request.method == 'GET':
        categories = Category.objects.select_related('parent')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    serializer = CategorySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


@extend_schema(
    tags=['Category'],
    summary='Retrieve, Update and Delete Category',
    description='Retrieve, update or delete a category using its ID.',
    parameters=[
        OpenApiParameter(
            name='pk',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='Category ID'
        )
    ],
    request=CategorySerializer,
    responses={
        200: CategorySerializer,
        204: OpenApiResponse(description='Category deleted successfully.'),
        400: OpenApiResponse(description='Validation error.'),
        404: OpenApiResponse(description='Category not found.')
    }
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def category_detail(request, pk):

    category = get_object_or_404(Category, pk=pk)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ==================================================
# PRODUCT API
# ==================================================

@extend_schema(
    tags=['Product'],
    summary='List and Create Products',
    description='Retrieve all products or create a new product.',
    request=ProductSerializer,
    responses={
        200: ProductSerializer(many=True),
        201: ProductSerializer,
        400: OpenApiResponse(description='Validation error.')
    }
)
@api_view(['GET', 'POST'])
def product_list_create(request):

    if request.method == 'GET':
        products = Product.objects.select_related(
            'brand',
            'category'
        ).prefetch_related(
            'images',
            'variants',
            'attributes'
        )

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


@extend_schema(
    tags=['Product'],
    summary='Retrieve, Update and Delete Product',
    description='Retrieve, update or delete a product using its ID.',
    parameters=[
        OpenApiParameter(
            name='pk',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='Product ID'
        )
    ],
    request=ProductSerializer,
    responses={
        200: ProductSerializer,
        204: OpenApiResponse(description='Product deleted successfully.'),
        400: OpenApiResponse(description='Validation error.'),
        404: OpenApiResponse(description='Product not found.')
    }
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_detail(request, pk):

    product = get_object_or_404(
        Product.objects.select_related(
            'brand',
            'category'
        ).prefetch_related(
            'images',
            'variants',
            'attributes'
        ),
        pk=pk
    )

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ==================================================
# PRODUCT IMAGE API
# ==================================================

@extend_schema(
    methods=['POST'],
    tags=['Product Image'],
    summary='Upload Product Image',
    request={
        'multipart/form-data': ProductImageSerializer
    },
    responses={201: ProductImageSerializer}
)
@extend_schema(
    methods=['GET'],
    tags=['Product Image'],
    summary='List Product Images',
    responses={200: ProductImageSerializer(many=True)}
)
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def product_image_list_create(request):

    if request.method == 'GET':
        images = ProductImage.objects.select_related('product')
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data)

    serializer = ProductImageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


@extend_schema(
    tags=['Product Image'],
    summary='Retrieve, Update and Delete Product Image',
    description='Retrieve, replace, partially update or delete a product image.',
    parameters=[
        OpenApiParameter(
            name='pk',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='Product image ID'
        )
    ],
    request={
        'multipart/form-data': ProductImageSerializer
    },
    responses={
        200: ProductImageSerializer,
        204: OpenApiResponse(description='Image deleted successfully.'),
        400: OpenApiResponse(description='Validation error.'),
        404: OpenApiResponse(description='Image not found.')
    }
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def product_image_detail(request, pk):

    image = get_object_or_404(ProductImage, pk=pk)

    if request.method == 'GET':
        serializer = ProductImageSerializer(image)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = ProductImageSerializer(
            image,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    image.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ==================================================
# PRODUCT VARIANT API
# ==================================================

@extend_schema(
    tags=['Product Variant'],
    summary='List and Create Product Variants',
    description='Retrieve all product variants or create a new variant.',
    request=ProductVariantSerializer,
    responses={
        200: ProductVariantSerializer(many=True),
        201: ProductVariantSerializer,
        400: OpenApiResponse(description='Validation error.')
    }
)
@api_view(['GET', 'POST'])
def product_variant_list_create(request):

    if request.method == 'GET':
        variants = ProductVariant.objects.select_related('product')
        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data)

    serializer = ProductVariantSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


@extend_schema(
    tags=['Product Variant'],
    summary='Retrieve, Update and Delete Product Variant',
    description='Retrieve, update or delete a product variant using its ID.',
    parameters=[
        OpenApiParameter(
            name='pk',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='Product variant ID'
        )
    ],
    request=ProductVariantSerializer,
    responses={
        200: ProductVariantSerializer,
        204: OpenApiResponse(description='Variant deleted successfully.'),
        400: OpenApiResponse(description='Validation error.'),
        404: OpenApiResponse(description='Variant not found.')
    }
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_variant_detail(request, pk):

    variant = get_object_or_404(ProductVariant, pk=pk)

    if request.method == 'GET':
        serializer = ProductVariantSerializer(variant)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = ProductVariantSerializer(
            variant,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    variant.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ==================================================
# PRODUCT ATTRIBUTE API
# ==================================================

@extend_schema(
    tags=['Product Attribute'],
    summary='List and Create Product Attributes',
    description='Retrieve all product attributes or create a new attribute.',
    request=ProductAttributeSerializer,
    responses={
        200: ProductAttributeSerializer(many=True),
        201: ProductAttributeSerializer,
        400: OpenApiResponse(description='Validation error.')
    }
)
@api_view(['GET', 'POST'])
def product_attribute_list_create(request):

    if request.method == 'GET':
        attributes = ProductAttribute.objects.select_related('product')
        serializer = ProductAttributeSerializer(attributes, many=True)
        return Response(serializer.data)

    serializer = ProductAttributeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


@extend_schema(
    tags=['Product Attribute'],
    summary='Retrieve, Update and Delete Product Attribute',
    description='Retrieve, update or delete a product attribute using its ID.',
    parameters=[
        OpenApiParameter(
            name='pk',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='Product attribute ID'
        )
    ],
    request=ProductAttributeSerializer,
    responses={
        200: ProductAttributeSerializer,
        204: OpenApiResponse(description='Attribute deleted successfully.'),
        400: OpenApiResponse(description='Validation error.'),
        404: OpenApiResponse(description='Attribute not found.')
    }
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_attribute_detail(request, pk):

    attribute = get_object_or_404(ProductAttribute, pk=pk)

    if request.method == 'GET':
        serializer = ProductAttributeSerializer(attribute)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = ProductAttributeSerializer(
            attribute,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    attribute.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
