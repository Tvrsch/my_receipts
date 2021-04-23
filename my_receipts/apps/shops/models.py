from django.db import models
from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")
        ordering = ("name", "address")
        unique_together = ("name", "address")
        index_together = ("name", "address")

    name = models.CharField(_("Name"), max_length=255, unique=True)
    address = models.TextField(_("Address"), blank=True)
    itn = models.PositiveBigIntegerField(_("Individual Taxpayer Number"), default=0)
    url = models.URLField(_("Url"), blank=True)

    def __str__(self):
        return self.name
