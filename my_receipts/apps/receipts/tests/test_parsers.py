from datetime import datetime
from pathlib import Path

from my_receipts.apps.receipts.parsers import TaxcomParser

CURRENT_DIR = Path(__file__).resolve(strict=True).parent


def test_taxcom(requests_mock):
    with open(CURRENT_DIR / "taxcom_page.html", encoding="utf8") as fp:
        html = fp.read()
    requests_mock.get(TaxcomParser.base_url, text=html)

    parser = TaxcomParser("00000000-0000-0000-0000-000000000000")

    assert parser.get_html() == html

    assert parser.shop_name == 'ООО "Лента"'
    assert parser.shop_itn == 7814148471
    assert parser.shop_address == "630083, Новосибирск, ул.Большевистская, д.52/1"
    assert parser.terminal_number == 29
    assert parser.shift == 204
    assert parser.cashier == "Оператор"
    assert parser.receipt_number == 59
    assert parser.receipt_created_dt == datetime(2021, 2, 17, 12, 13)
    assert parser.receipt_sum == 1196.00
    assert len(parser.items) == 16

    item = parser.items[2]
    assert item.name == "Пакет ЛЕНТА майка 9кг"
    assert item.price == 3.49
    assert item.amount == 1.0
    assert item.sum == 3.49
