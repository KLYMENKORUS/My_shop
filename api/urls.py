from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('orders/items', views.order_items),
    path('order/<int:pk>/', views.OrderItemDetail.as_view()),
    path('orders/', views.order_item),
    path('product/<int:pk>/', views.ProductDetailView.as_view()),
    path('product/', views.product),
]