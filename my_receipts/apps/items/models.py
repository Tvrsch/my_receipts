from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Item(models.Model):
    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
        ordering = ("name",)

    name = models.CharField(_("General name"), max_length=255, unique=True)

    def __str__(self):
        return self.name

    def clean(self):
        if ItemName.objects.filter(name=self.name).exists():
            raise ValidationError(
                {
                    "name": _("ItemName already exist with name '%(name)s'")
                    % {"name": self.name}
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Item, self).save(*args, **kwargs)


class ItemName(models.Model):
    class Meta:
        verbose_name = _("Item sub name")
        verbose_name_plural = _("Item sub names")
        ordering = ("name",)

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="names")
    name = models.CharField(_("Sub name"), max_length=255, db_index=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ItemName, self).save(*args, **kwargs)

    def clean(self):
        query = ItemName.objects
        if self.id:
            query = query.exclude(id=self.id)
        if query.filter(name=self.name).exists():
            raise ValidationError(
                {
                    "name": _("Name '%(name)s' already exists for item '%(item)s'")
                    % {"name": self.name, "item": self.item}
                }
            )

    @classmethod
    def get_or_create_item(cls, name):
        try:
            item = cls.objects.get(name=name).item
        except cls.DoesNotExist:
            item = Item.objects.create(name=name)
            cls.objects.create(name=name, item=item)
        return item
