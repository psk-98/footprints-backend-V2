from rest_framework import serializers

from .models import Address, Order, OrderItem

from accounts.serializers import UserSerializer
from product.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    
    item = ProductSerializer()

    class Meta:
        model = OrderItem
        depth = 2
        fields = [
            'id',
            'quantity',
            'item',
            'size'
        ]

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    
    order_items = OrderItemSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Order
        depth = 1
        fields = [
            "user",
            "order_items"
        ]