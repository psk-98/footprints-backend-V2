from rest_framework import serializers

from .models import Product, ProductStock, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = [
            'get_image',
            'id',
            'image',
            'product'
        ]

class StockSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductStock
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    product_stock = StockSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'name',
            'slug',
            'get_absolute_url',
            'description',
            'price',
            'discount_price',
            'product_images',
            'product_stock',
        ]
        extra_kwargs = {'images': {'write_only': True}}

