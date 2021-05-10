from django.contrib import admin

from . import models


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "receipts_count")
    list_filter = ("name",)
