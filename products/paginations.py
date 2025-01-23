from django.utils.translation import gettext_lazy as _
from rest_framework.pagination import LimitOffsetPagination


class BaseLimitOffsetPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.products_json = self.products(queryset)
        # self.custom_json = self.custom(queryset)
        return super(BaseLimitOffsetPagination, self).paginate_queryset(
            queryset, request, view
        )


class GeneralPaginations(BaseLimitOffsetPagination):
    def products(self, queryset):
        return queryset

    def custom(self, queryset):
        qs = queryset.values()
        return qs

    def get_paginated_response(self, data):
        paginated_response = super(GeneralPaginations, self).get_paginated_response(
            data
        )
        return paginated_response
