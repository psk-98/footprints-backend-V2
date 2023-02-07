from rest_framework import serializers
from django.db.models import QuerySet

from .models import Product, ProductStock, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = ProductImage
        fields = [
            'get_image',
        ]
    

class StockSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductStock
        fields = [
            'size',
            'amount_in_stock',
        ]


class SimilarProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    product_stock = StockSerializer(many=True)

    
    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'slug',
            'price',
            'discount_price',
            'product_images',
            'product_stock',

        ]
        extra_kwargs = {'images': {'write_only': True}}


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    product_stock = StockSerializer(many=True)
    similar = serializers.SerializerMethodField()

    
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
            'similar',

        ]
        extra_kwargs = {'images': {'write_only': True}}
    
    def get_similar(self, obj):
        similar_objects = obj.tags.similar_objects()
  
        serializers = SimilarProductSerializer(similar_objects, many=True)
    
        return serializers.data


