import uuid

from concurrency.fields import AutoIncVersionField, IntegerVersionField
from concurrentsafedelete.models import ConcurrentSafeDeleteModel
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModelBase, RulesModelMixin
from safedelete.models import SOFT_DELETE_CASCADE
from products.rules import can_add_product, can_view_product, can_update_product, can_delete_product


class Product(RulesModelMixin, ConcurrentSafeDeleteModel, metaclass=RulesModelBase):

    _safedelete_policy = SOFT_DELETE_CASCADE

    version = IntegerVersionField()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(
        max_length=200, help_text="Required. Max length is 200.", null=True
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField("Date created", auto_now_add=True)
    updated_at = models.DateTimeField("Date updated", auto_now=True)

    class Meta:
        rules_permissions = {
            "view": can_view_product,
            "add": can_add_product,
            "change": can_update_product,
            "delete": can_delete_product,
            "list": can_view_product,
        }

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, force_policy=None, **kwargs): 
        result = super().delete(force_policy=force_policy, **kwargs)
        return result

    def undelete(self, force_policy=None, **kwargs): 
        result = super().undelete(force_policy=force_policy, **kwargs)
        return result
