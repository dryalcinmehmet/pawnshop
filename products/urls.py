from products.views import ProductViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=True)

router.register(r"", ProductViewSet, basename="products-viewset")

urlpatterns = [path("", include(router.urls))]
