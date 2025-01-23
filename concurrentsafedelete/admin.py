from django.contrib import admin
from safedelete.admin import SafeDeleteAdmin
from django.contrib import messages

class ConcurrentSafeDeleteAdmin(SafeDeleteAdmin):
    actions = ['undelete_selected']

    @admin.action(description="Undelete selected objects")
    def undelete_selected(self, request, queryset):
        undeleted_count = 0
        for obj in queryset:
            if hasattr(obj, 'undelete') and obj.deleted:  # Sadece silinmiş olan objeleri kontrol et
                obj.undelete()
                undeleted_count += 1
        if undeleted_count > 0:
            self.message_user(
                request, f"{undeleted_count} objects successfully undeleted.", messages.SUCCESS
            )
        else:
            self.message_user(
                request, "No deleted objects were found to undelete.", messages.WARNING
            )