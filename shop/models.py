from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Модель описания категории товара"""
    name = models.CharField(verbose_name=_('name'), max_length=200, db_index=True)
    slug = models.SlugField(verbose_name=_('slug'), max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    """Модель описания товара"""
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE,
                                 verbose_name=_('category'))
    name = models.CharField(verbose_name=_('name'), max_length=200, db_index=True)
    slug = models.SlugField(verbose_name=_('slug'), max_length=200, db_index=True)
    image_product = models.ImageField(verbose_name=_('image product'), upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(verbose_name=_('description'), blank=True)
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=2)
    available = models.BooleanField(verbose_name=_('available'), default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    @property
    def get_photo_url(self):
        if self.image_product and hasattr(self.image_product, 'url'):
            return self.image_product.url
        else:
            return '/static/images/no_image.png'
