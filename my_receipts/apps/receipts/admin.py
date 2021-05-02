from django.contrib import admin

from . import models


class ReceiptItemInline(admin.StackedInline):
    model = models.ReceiptItem
    extra = 0
    fields = (
        "item",
        "price",
        "amount",
        "sum",
    )
    readonly_fields = (
        "item",
        "price",
        "amount",
        "sum",
    )


@admin.register(models.Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "remote_id",
        "vendor",
        "created_in_receipt",
        "sum",
    )
    inlines = (ReceiptItemInline,)
