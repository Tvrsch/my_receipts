from django.contrib import admin

from . import actions, models


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "is_removed", "receipts_count")
    list_filter = (
        "name",
        "is_removed",
    )
    actions = (actions.MergeShops.request_handler,)

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model.all_objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


@admin.register(models.ReplaceAddressRule)
class ReplaceAddressRuleAdmin(admin.ModelAdmin):
    pass
