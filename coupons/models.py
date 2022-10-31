from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    code = models.CharField(verbose_name=_('code'), max_length=50, unique=True)
    valid_from = models.DateTimeField(verbose_name=_('valid from'))
    valid_to = models.DateTimeField(verbose_name=_('valid to'))
    discount = models.IntegerField(verbose_name=_('discount'),
                                   validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(verbose_name=_('active'))

    def __str__(self):
        return self.code
