import re
from datetime import datetime
from typing import List

import requests

from ..models import Receipt
from .base import HTMLParser, Item
from .errors import ParserError, ReceiptNotFound

INT_REGEX = re.compile(r"\d+")


class BadResponse(ParserError):
    pass


class TaxcomParser(HTMLParser):
    vendor = Receipt.Vendor.TAXCOM
    base_url = "https://receipt.taxcom.ru/v01/show"

    def __init__(self, id):
        super(TaxcomParser, self).__init__()
        self.id = id

    def check_soup(self, soup):
        if self._soup.find("div", attrs={"class": "notfound"}):
            raise ReceiptNotFound(f"Receipt with id '{self.id}' not found")

    def get_html(self):
        return requests.get(self.base_url, params={"id": self.id}).text

    def get_shop_name(self):
        receipt_subtitle = self.soup.find(
            name="span", attrs={"class": "receipt-subtitle"}
        )
        shop_name = receipt_subtitle.text.strip()
        self._data["shop_name"] = shop_name
        return shop_name

    def get_shop_itn(self):
        shop_itn = self.soup.find(name="span", attrs={"class": "receipt-value-1018"})
        return int(INT_REGEX.search(shop_itn.text).group())

    def get_shop_address(self):
        shop_address = self.soup.find("span", attrs={"class": "receipt-value-1009"})
        return shop_address.text.strip()

    def get_terminal_number(self) -> int:
        terminal_number = self.soup.find(
            "span", attrs={"class": "receipt-value-1187"}
        ).find("span")
        return int(INT_REGEX.search(terminal_number.text).group())

    def get_shift(self) -> int:
        shift = self.soup.find("span", attrs={"class": "receipt-value-1038"})
        return int(shift.text.strip())

    def get_cashier(self) -> str:
        cashier = self.soup.find("span", attrs={"class": "receipt-value-1021"})
        return cashier.text.strip()

    def get_receipt_number(self) -> int:
        receipt_number = self.soup.find("span", attrs={"class": "receipt-value-1042"})
        return int(receipt_number.text.strip())

    def get_receipt_created_dt(self) -> datetime:
        receipt_created_dt = self.soup.find(
            "span", attrs={"class": "receipt-value-1012"}
        )  # 09.05.21 15:48
        return datetime.strptime(receipt_created_dt.text.strip(), "%d.%m.%y %H:%M")

    def get_items(self) -> List[Item]:
        items = []
        for item in self.soup.find_all("div", attrs={"class": "item"}):
            items.append(
                Item(
                    name=item.find(
                        "span", attrs={"class": "receipt-value-1030"}
                    ).text.strip(),
                    price=float(
                        item.find(
                            "span", attrs={"class": "receipt-value-1079"}
                        ).text.strip()
                    ),
                    amount=float(
                        item.find(
                            "span", attrs={"class": "receipt-value-1023"}
                        ).text.strip()
                    ),
                    sum=float(
                        item.find(
                            "span", attrs={"class": "receipt-value-1043"}
                        ).text.strip()
                    ),
                )
            )
        return items

    def get_receipt_sum(self) -> float:
        receipt_sum = self.soup.find("span", attrs={"class": "receipt-value-1020"})
        return float(receipt_sum.text)
