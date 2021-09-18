from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django.contrib.admin import helpers
from django.contrib.admin.utils import model_ngettext
from django.shortcuts import render


def merge_shops(modeladmin, request, queryset):
    """Merge two shops with similar addresses"""
    if request.POST.get("merge_shops"):
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
    else:
        title = "Merging"
        objects_name = model_ngettext(queryset)
        (
            merging_objects,
            model_count,
            perms_needed,
            protected,
        ) = modeladmin.get_deleted_objects(queryset, request)
        opts = modeladmin.model._meta
        context = {
            **modeladmin.admin_site.each_context(request),
            "title": title,
            "objects_name": str(objects_name),
            "merging_objects": [merging_objects],
            "model_count": dict(model_count).items(),
            "queryset": queryset,
            "opts": opts,
            "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
            "media": modeladmin.media,
        }

        request.current_app = modeladmin.admin_site.name

        # Display the confirmation page
        return render(request, "shops/confirm_merge.html", context)


merge_shops.short_description = _("Merge second shop to first")
