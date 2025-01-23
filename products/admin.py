from django.contrib import admin
from rules.contrib.admin import ObjectPermissionsModelAdmin
from safedelete.admin import SafeDeleteAdmin, highlight_deleted

from . import models
from concurrentsafedelete.admin import ConcurrentSafeDeleteAdmin


class ProductAdmin(ConcurrentSafeDeleteAdmin):
    list_display = (
        highlight_deleted,
            "id",
            "name",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
    ) + SafeDeleteAdmin.list_display

    list_filter = (
            "id",
            "name",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
    ) + SafeDeleteAdmin.list_filter
    date_hierarchy = "updated_at"
    search_fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
    )
    ordering = ("-updated_at",)


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Product, ProductAdmin)
