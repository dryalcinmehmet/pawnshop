from concurrency.api import concurrency_disable_increment
from django.contrib.admin.utils import NestedObjects
from django.db import models, router
from django.utils import timezone
from safedelete.config import (
    HARD_DELETE,
    HARD_DELETE_NOCASCADE,
    NO_DELETE,
    SOFT_DELETE,
    SOFT_DELETE_CASCADE,
)
from safedelete.models import SafeDeleteModel, is_safedelete_cls
from safedelete.signals import post_softdelete, pre_softdelete
from safedelete.utils import can_hard_delete, related_objects


class ConcurrentSafeDeleteModel(SafeDeleteModel):
    class Meta:
        abstract = True

    def undelete(self, force_policy=None, **kwargs):
        """Undelete a soft-deleted model.

        Args:
            force_policy: Force a specific undelete policy. (default: {None})
            kwargs: Passed onto :func:`save`.

        .. note::
            Will raise a :class:`AssertionError` if the model was not soft-deleted.
        """
        current_policy = force_policy or self._safedelete_policy

        assert self.deleted
        with concurrency_disable_increment(self):
            self.save(keep_deleted=False, **kwargs)

        if current_policy == SOFT_DELETE_CASCADE:
            for related in related_objects(self):
                if is_safedelete_cls(related.__class__) and related.deleted:
                    related.undelete()
        return self, None  # Eklenen dönüş

    def delete(self, force_policy=None, **kwargs):
        """Overrides Django's delete behaviour based on the model's delete policy.

        Args:
            force_policy: Force a specific delete policy. (default: {None})
            kwargs: Passed onto :func:`save` if soft deleted.
        """
        current_policy = (
            self._safedelete_policy if (force_policy is None) else force_policy
        )

        try:
            self.is_active = False
        except AttributeError:
            pass

        if current_policy == NO_DELETE:

            # Don't do anything.
            return

        elif current_policy == SOFT_DELETE:

            # Only soft-delete the object, marking it as deleted.
            self.deleted = timezone.now()
            using = kwargs.get("using") or router.db_for_write(
                self.__class__, instance=self
            )
            # send pre_softdelete signal
            pre_softdelete.send(sender=self.__class__, instance=self, using=using)
            with concurrency_disable_increment(self):
                self.save(keep_deleted=True, **kwargs)
            # send softdelete signal
            post_softdelete.send(sender=self.__class__, instance=self, using=using)

        elif current_policy == HARD_DELETE:

            # Normally hard-delete the object.
            super(SafeDeleteModel, self).delete()

        elif current_policy == HARD_DELETE_NOCASCADE:

            # Hard-delete the object only if nothing would be deleted with it

            if not can_hard_delete(self):
                self.delete(force_policy=SOFT_DELETE, **kwargs)
            else:
                self.delete(force_policy=HARD_DELETE, **kwargs)

        elif current_policy == SOFT_DELETE_CASCADE:
            # Soft-delete on related objects before
            for related in related_objects(self):
                if is_safedelete_cls(related.__class__) and not related.deleted:
                    related.delete(force_policy=SOFT_DELETE, **kwargs)

            collector = NestedObjects(using=router.db_for_write(self))
            collector.collect([self])
            # update fields (SET, SET_DEFAULT or SET_NULL)
            for model, instances_for_fieldvalues in collector.field_updates.items():
                for (field, value), instances in instances_for_fieldvalues.items():
                    query = models.sql.UpdateQuery(model)
                    query.update_batch(
                        [obj.pk for obj in instances],
                        {field.name: value},
                        collector.using,
                    )

            # soft-delete the object
            self.delete(force_policy=SOFT_DELETE, **kwargs)
                    
        return self, None  # Eklenen dönüş
