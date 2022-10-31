from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path("admin/", admin.site.urls),

] + i18n_patterns(
    path("i18n/", include("django.conf.urls.i18n")),
    path("cart/", include('cart.urls', namespace='cart')),
    path("orders/", include('orders.urls', namespace='orders')),
    path("payment/", include("payment.urls", namespace='payment')),
    path("coupons/", include("coupons.urls", namespace="coupons")),
    path("api/", include("api.urls", namespace="api")),
    path("", include('shop.urls', namespace='shop')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
