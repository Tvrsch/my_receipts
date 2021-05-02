import pytest
from django.core.exceptions import ValidationError

from my_receipts.apps.items.models import Item, ItemName

pytestmark = pytest.mark.django_db


def test_items():
    name = "Bread"
    bread = ItemName.get_or_create_item(name)
    assert str(bread) == name
    assert bread == ItemName.get_or_create_item(name)


def test_clean():
    name = "Bread2"
    item = ItemName.get_or_create_item(name)
    with pytest.raises(ValidationError):
        Item.objects.create(name=name)
    with pytest.raises(ValidationError):
        ItemName.objects.create(name=name, item=item)

    item_name = item.names.first()
    assert item_name
    item_name.name += "-"
    item_name.save()
