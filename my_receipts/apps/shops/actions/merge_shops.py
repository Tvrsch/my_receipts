from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext


def merge_shops(modeladmin, request, queryset):
    """Merge two shops with similar addresses"""
    count = queryset.count()
    if count != 2:
        message = _("It's possible to merge only 2 shops, not %(count)s") % {
            "count": count
        }
        modeladmin.message_user(request, message, level=messages.ERROR)
    else:
        master, slave = queryset.all()
        receipts_updated = slave.receipts.update(shop=master)
        slave.is_removed = True
        slave.save()

        message = (
            ngettext(
                "%(count)d receipts moved to one shop.",
                "%(count)d receipts moved to one shop.",
                receipts_updated,
            )
            % {"count": receipts_updated}
        )
        modeladmin.message_user(request, message)


merge_shops.short_description = _("Merge second shop to first")
