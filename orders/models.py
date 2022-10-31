from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    """Модель заказа"""
    first_name = models.CharField(verbose_name=_('first name'), max_length=50)
    last_name = models.CharField(verbose_name=_('last name'), max_length=50)
    email = models.EmailField(verbose_name=_('email'))
    address = models.CharField(verbose_name=_('address'), max_length=250)
    postal_code = models.CharField(verbose_name=_('postal code'), max_length=20)
    city = models.CharField(verbose_name=_('city'), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(verbose_name=_('paid'), default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True,
                               on_delete=models.SET_NULL, verbose_name=_('coupon'))
    discount = models.IntegerField(verbose_name=_('discount'), default=0, validators=[MinValueValidator(0),
                                                                                      MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_const(self):
        total_const = sum(item.get_cost() for item in self.items.all())
        return total_const - total_const * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    """Модель сохранения товара в корзине"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items',
                                verbose_name=_('product'))
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'), default=1)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity
