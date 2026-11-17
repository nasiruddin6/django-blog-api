from django.urls import path
from . import views


urlpatterns = [
    # Brand
    path('brands/', views.brand_list_create),
    path('brands/<int:pk>/', views.brand_detail),

    # Category
    path('categories/', views.category_list_create),
    path('categories/<int:pk>/', views.category_detail),

    # Product
    path('products/', views.product_list_create),
    path('products/<int:pk>/', views.product_detail),

    # Product Images
    path('product-images/', views.product_image_list_create),
    path('product-images/<int:pk>/', views.product_image_detail),

    # Product Variants
    path('product-variants/', views.product_variant_list_create),
    path('product-variants/<int:pk>/', views.product_variant_detail),

    # Product Attributes
    path('product-attributes/', views.product_attribute_list_create),
    path('product-attributes/<int:pk>/', views.product_attribute_detail),
]
