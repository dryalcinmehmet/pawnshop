from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rules.contrib.admin import ObjectPermissionsModelAdmin
from safedelete.admin import SafeDeleteAdmin, highlight_deleted
from users.models import User

from . import models


class UserAdmin(SafeDeleteAdmin):
    list_display = (
        highlight_deleted,
        "id",
        "email",
        "first_name",
        "last_name",
    )

    list_filter = ("id",  "email", "first_name", "last_name")
    search_fields = ("id",  "email", "first_name", "last_name")
    ordering = ("-id",)


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.User, UserAdmin)
