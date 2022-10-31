from rest_framework import serializers
from shop.models import Product
from orders.models import OrderItem, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'description', 'price', 'created', 'image_product')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'price', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'first_name', 'last_name', 'email', 'city', 'address', 'created',
                  'paid', 'coupon', 'braintree_id', 'discount')


