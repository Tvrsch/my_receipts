from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django.contrib.admin import helpers
from django.shortcuts import render

from my_receipts.apps.receipts.models import Receipt


def check_queryset(queryset):
    count = queryset.count()
    if count != 2:
        message = _(f"It's possible to merge only 2 shops, not {count}")
        return message


def get_merge_confirmation_context(modeladmin, request, queryset):
    master, slave = queryset.all()
    opts = modeladmin.model._meta
    receipts_count = Receipt.objects.filter(shop=slave).count()
    context = {
        **modeladmin.admin_site.each_context(request),
        "title": "Merging",
        "master": master,
        "slave": slave,
        "slave_receipts": receipts_count,
        "queryset": queryset,
        "opts": opts,
        "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
        "media": modeladmin.media,
    }
    return context


def do_merge(queryset):
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
    return message


def merge_shops(modeladmin, request, queryset):
    print(f"request: {request}")
    """Merge two shops with similar addresses"""
    error_message = check_queryset(queryset)
    if error_message:
        modeladmin.message_user(request, error_message, level=messages.ERROR)
        return
    if request.POST.get("merge_shops"):
        success_message = do_merge(queryset)
        modeladmin.message_user(request, success_message)
    else:
        request.current_app = modeladmin.admin_site.name
        context = get_merge_confirmation_context(modeladmin, request, queryset)
        # Display the confirmation page
        return render(request, "shops/merge_shops_confirmation.html", context)


merge_shops.short_description = _("Merge second shop to first")
