from products.models import Product
from django_filters import IsoDateTimeFilter, OrderingFilter
from django_filters import rest_framework as filters


class ProductFilter(filters.FilterSet):
    order_by = OrderingFilter(
        # tuple-mapping retains order
        fields=(("created_at", "created_at"))
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
        ]
