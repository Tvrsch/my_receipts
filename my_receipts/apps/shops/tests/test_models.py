import pytest
from django.db import transaction
from django.db.utils import IntegrityError
from model_bakery import baker

from my_receipts.apps.shops.models import Shop

pytestmark = pytest.mark.django_db

MODEL = "shops.Shop"


def test_shop_unique():

    lenta = baker.make(MODEL, name='ООО "Лента"', itn=7814148471)
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            baker.make(MODEL, name=lenta.name)
    baker.make(
        MODEL,
        name=lenta.name,
        address="Россия, 630083, Новосибирская обл., г. Новосибирск, ул.Большевистская, д.52/1",
    )

    assert Shop.objects.get(name=lenta.name, address="") == lenta


def test_shop_strip_name_and_address():
    lenta = baker.make(MODEL, name='ООО "Лента"')
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            baker.make(MODEL, name=f"  {lenta.name}  ", address="  ")


def test_shop_str():
    name = 'ООО "Лента"'
    lenta = baker.make(MODEL, name=name)
    assert str(lenta) == name
