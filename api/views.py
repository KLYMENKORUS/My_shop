from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from shop.models import Product
from orders.models import OrderItem, Order
from .serializers import ProductSerializer, OrderItemSerializer, OrderSerializer


@api_view(['GET'])
def product(request):
    if request.method == 'GET':
        product_api = Product.objects.filter(available=True)[:5]
        serializer = ProductSerializer(product_api, many=True)
        return Response(serializer.data)


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer


@api_view(['GET'])
def order_item(request):
    if request.method == 'GET':
        order_item_api = OrderItem.objects.filter(product__available=True)[:10]
        serializer = OrderItemSerializer(order_item_api, many=True)
        return Response(serializer.data)


class OrderItemDetail(RetrieveAPIView):
    queryset = OrderItem.objects.filter(product__available=True)
    serializer_class = OrderItemSerializer


@api_view(['GET'])
def order_items(request):
    if request.method == 'GET':
        order_items_api = Order.objects.filter(items__product__available=True)[:10]
        serializer = OrderSerializer(order_items_api, many=True)
        return Response(serializer.data)
