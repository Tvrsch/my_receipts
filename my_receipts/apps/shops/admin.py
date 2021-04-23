from django.contrib import admin

from . import models


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "url")
    list_filter = ("name",)
