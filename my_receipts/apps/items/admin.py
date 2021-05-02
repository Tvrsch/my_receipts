from django.contrib import admin

from . import models


class NamesInline(admin.StackedInline):
    model = models.ItemName
    extra = 1
    fields = ("name",)


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = (NamesInline,)
