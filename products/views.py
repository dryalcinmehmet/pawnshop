from django.utils.translation import gettext_lazy as _
from django_auto_prefetching import AutoPrefetchViewSetMixin
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from jsonschema import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rules.contrib.rest_framework import AutoPermissionViewSetMixin
from products.filters import ProductFilter
from products.models import Product
from products.paginations import GeneralPaginations
from products.serializers import (
    ProductCreateSerializer,
    ProductListOrDetailSerializer,
    ProductSerializer,
    ProductUpdateSerializer,
    ProductDeleteSerializer,
)


class ProductViewSet(
    AutoPermissionViewSetMixin, AutoPrefetchViewSetMixin, viewsets.ModelViewSet
):
    queryset = Product.objects.none()
    serializer_class = ProductCreateSerializer
    serializer_action_classes = {
        "list": ProductSerializer,
        "create": ProductCreateSerializer,
        "retrieve": ProductListOrDetailSerializer,
        "update": ProductUpdateSerializer,
        "partial_update": ProductUpdateSerializer,
        "destroy": ProductDeleteSerializer,
    }
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    http_method_names = ["options", "get", "post", "put", "patch", "delete"]
    pagination_class = GeneralPaginations

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        "list": "list",
        "destroy": "destroy",
    }

    def get_queryset(self):
        # handle anonymous user case to aid in schema generation
        qs = Product.objects.all()
        if not self.request:
            return self.queryset.none()
        elif self.request.user.is_active:
            queryset = qs
        elif self.request.user.is_superuser:
            queryset = qs
        else:
            return self.queryset.none()
        return queryset

    def list(self, request):
        """
        **List all Product requests related to the user.**

        User should be *authenticated* and have an *active* (is_active=True) account.

        **Roles required**: Staff and/or Admin

        """
        return super().list(request)

    def retrieve(self, request, *args, **kwargs):
        """
        **Get a specific Production Site request details.**

        User should be *authenticated* and have an *active* (is_active=True) account.

        **Roles required**: Staff and/or Admin



        """
        return super().retrieve(request, *args, **kwargs)

    def create(self, request):
        """
        **Create a specific production site.**

        User should be *authenticated* and have an *active* (is_active=True) account.

        **Roles required**: Staff and/or Admin

        **User employed by an active allowed organization**: Grid Operator
        """
        return super().create(request)

    def update(self, request, pk=None, *args, **kwargs):
        """
        **Upsert a specific production site.**

        User should be *authenticated* and have an *active* (is_active=True) account.

        **Note:** Production sites should be associated to a producer managed by the user.

        **Roles required**: Staff and/or Admin

        **User employed by an active allowed organization**: Grid Operator
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        **Update a specific production site.**

        User should be *authenticated* and have an *active* (is_active=True) account.

        ****Note:**** Object should be owned by the user's organization or retailer.

        **Roles required**: Staff and/or Admin

        **User employed by an active allowed organization**: Grid Operator
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        **Delete a specific Production Site.**

        User should be *authenticated* and have an *active* (is_active=True) account.

        **Note:** Object should be owned by the user.

        **Roles required**: Admin

        **User employed by an active allowed organization**: Consumer or Retailer
        """
        instance = self.get_object()
        instance.delete()  # Delete metodunu doğru bir şekilde çağırdığınızdan emin olun
        return Response({"response": {"status": "Product deleted."}})

    @extend_schema(
        # change the serializer the schema generator uses for the response.
        # Fixes an rtype issue in the generated API client sdk
        request=ProductSerializer,
        methods=["POST"],
    )
    @action(detail=False, methods=["post"], url_path="test-here")
    def custom_function(self, request, *args, **kwargs):
        """
        **Add product by custom method .**

        User should be *authenticated* and have an *active* (is_active=True) account.

        **Note:** Object should be owned by the user's organization or retailer.

        **Roles required**: Staff and/or Admin

        **User employed by an active allowed organization**: Retailer
        """

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Get producer and retailer objects using the UUID of the producer supplied by the user
            name = serializer.validated_data["name"]
            description = serializer.validated_data["description"]

            # Do something
            return Response({"response": {"status": "Product added."}})
