from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel


class Shop(SoftDeletableModel):
    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")
        ordering = ("name", "address")
        unique_together = ("name", "address")
        index_together = ("name", "address")

    name = models.CharField(_("Name"), max_length=255)
    address = models.TextField(_("Address"), blank=True)
    itn = models.PositiveBigIntegerField(_("Individual Taxpayer Number"), default=0)
    url = models.URLField(_("Url"), blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        self.address = self.address.strip()
        super(Shop, self).save(*args, **kwargs)

    @property
    def receipts_count(self):
        return self.receipts.count()

    @staticmethod
    def prepare_address(address):
        if address:
            for old_text, new_text in ReplaceAddressRule.objects.values_list(
                "old_text", "new_text"
            ):
                address = address.replace(old_text, new_text)
        return address.strip()


class ReplaceAddressRule(models.Model):
    old_text = models.CharField(_("Old text"), max_length=128, unique=True)
    new_text = models.CharField(_("New text"), max_length=128, blank=True)

    class Meta:
        verbose_name = _("Replace address rule")
        verbose_name_plural = _("Replace address rules")

    def __str__(self):
        return f"{self.old_text!r} -> {self.new_text!r}"
