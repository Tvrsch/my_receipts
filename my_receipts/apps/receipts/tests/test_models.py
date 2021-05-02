from datetime import datetime

import pytest
from django.utils import timezone
from model_bakery import baker

from my_receipts.apps.receipts import models

pytestmark = pytest.mark.django_db


def test_receipts():
    receipt_defaults = {
        "vendor": models.Receipt.Vendor.TAXCOM,
        "remote_id": "00000000-0000-0000-0000-000000000000",
        "number": 189,
        "shift": 37,
        "cashier": "Оператор клиентского сервиса",
        "created_in_receipt": datetime(2021, 5, 1, 17, 52, tzinfo=timezone.utc),
        "sum": 2336.71,
    }
    receipt_items = (
        {
            "item_name": "Томаты черри красные тепличные 250г",
            "price": 194.99,
            "amount": 1,
            "sum": 194.99,
        },
        {
            "item_name": "Лимоны вес 1кг",
            "price": 159.99,
            "amount": 0.236,
            "sum": 37.76,
        },
        {
            "item_name": "Лаймы вес 1кг",
            "price": 469.99,
            "amount": 0.156,
            "sum": 73.32,
        },
    )

    lenta = baker.make("shops.Shop", name='ООО "Лента"', itn=7814148471)
    receipt_defaults["shop"] = lenta

    testUser = baker.make("users.User", email="testuser@test.com", username="testuser")
    receipt_defaults["user"] = testUser

    receipt = models.Receipt.objects.create(**receipt_defaults)
    assert str(receipt) == f"{receipt.vendor} [{receipt.remote_id}]"

    for order, item in enumerate(receipt_items, 1):
        item["order"] = order
        receipt.add_item(**item)
    assert receipt.receipt_items.count() == len(receipt_items)

    receipt_item = receipt.add_item(
        item_name="Пакет ЛЕНТА майка 9кг", price=4.49, amount=2
    )
    assert (
        str(receipt_item)
        == f"{receipt_item.item.name} {receipt_item.amount}x{receipt_item.price}"
    )
    assert receipt_item.sum == 8.98
    assert receipt_item.order == len(receipt_items) + 1
