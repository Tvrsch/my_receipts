from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from my_receipts.apps.items.models import ItemName


class Receipt(TimeStampedModel):
    class Meta:
        verbose_name = _("Receipt")
        verbose_name_plural = _("Receipts")
        ordering = ("created",)
        unique_together = ("vendor", "remote_id")
        index_together = ("vendor", "remote_id")

    class Vendor(models.TextChoices):
        TAXCOM = "taxcom", _("TaxCom")

    vendor = models.CharField(
        _("Vendor"), max_length=10, choices=Vendor.choices, db_index=True
    )
    remote_id = models.CharField(_("Remote id"), max_length=36, db_index=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="receipts"
    )
    shop = models.ForeignKey(
        "shops.Shop", on_delete=models.CASCADE, related_name="receipts"
    )

    number = models.PositiveIntegerField(_("Receipt number"), null=True, blank=True)
    shift = models.PositiveIntegerField(_("Shift"), null=True, blank=True)
    cashier = models.CharField(_("Cashier"), max_length=255, blank=True)
    created_in_receipt = models.DateTimeField(
        _("Created in receipt"), null=True, blank=True
    )
    sum = models.FloatField(_("Sum"))

    def add_item(self, item_name, price, amount, sum=None, order=None):
        item = ItemName.get_or_create_item(item_name)
        if sum is None:
            sum = price * amount
        if order is None:
            order = self.receipt_items.count() + 1
        receipt_item = ReceiptItem.objects.create(
            receipt=self, item=item, order=order, price=price, amount=amount, sum=sum
        )
        return receipt_item

    def __str__(self):
        return f"{self.vendor} [{self.remote_id}]"


class ReceiptItem(models.Model):
    class Meta:
        verbose_name = _("Receipt")
        verbose_name_plural = _("Receipts")
        ordering = ("order",)

    receipt = models.ForeignKey(
        Receipt, on_delete=models.CASCADE, related_name="receipt_items"
    )
    item = models.ForeignKey(
        "items.Item", on_delete=models.CASCADE, related_name="receipt_items"
    )
    order = models.PositiveSmallIntegerField(_("Order"), default=0)
    price = models.FloatField(_("Price"))
    amount = models.FloatField(_("Amount"))
    sum = models.FloatField(_("Sum"))

    def __str__(self):
        return f"{self.item.name} {self.amount}x{self.price}"
