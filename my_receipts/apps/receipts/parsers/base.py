from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup


@dataclass
class Item:
    name: str
    price: float
    amount: float
    sum: float


class HTMLParser:
    vendor = None
    base_url = None
    bs_kwargs = {"features": "html.parser"}

    _soup = None
    _data = {}

    def __init__(self):
        if self.vendor is None:
            raise ValueError("'vendor' is empty")

    @abstractmethod
    def get_html(self) -> str:
        """Returns receipt html page"""

    @abstractmethod
    def get_shop_name(self) -> str:
        """Returns shop name"""

    @abstractmethod
    def get_shop_itn(self) -> int:
        """Returns shop Individual Taxpayer Number"""

    @abstractmethod
    def get_shop_address(self) -> str:
        """Returns shop address"""

    @abstractmethod
    def get_terminal_number(self) -> str:
        """Returns cashier name"""

    @abstractmethod
    def get_shift(self) -> int:
        """Returns receipt shift"""

    @abstractmethod
    def get_cashier(self) -> str:
        """Returns cashier name"""

    @abstractmethod
    def get_receipt_number(self) -> int:
        """"Returns receipt number"""

    @abstractmethod
    def get_receipt_created_dt(self) -> datetime:
        """Returns receipt created datetime"""

    @abstractmethod
    def get_items(self) -> List[Item]:
        """Returns receipt items"""

    @abstractmethod
    def get_receipt_sum(self) -> float:
        """Returns receipt sum"""

    @property
    def soup(self):
        if self._soup is None:
            html = self.get_html()
            self._soup = BeautifulSoup(html, **self.bs_kwargs)
        return self._soup

    def __getitem__(self, item):
        if item not in self._data:
            try:
                value = getattr(self, f"get_{item}")()
            except AttributeError:
                raise KeyError(item)
            self._data[item] = value
        return self._data[item]

    @property
    def shop_name(self):
        return self["shop_name"]

    @property
    def shop_itn(self):
        return self["shop_itn"]

    @property
    def shop_address(self):
        return self["shop_address"]

    @property
    def terminal_number(self):
        return self["terminal_number"]

    @property
    def shift(self):
        return self["shift"]

    @property
    def cashier(self):
        return self["cashier"]

    @property
    def receipt_number(self):
        return self["receipt_number"]

    @property
    def receipt_created_dt(self):
        return self["receipt_created_dt"]

    @property
    def items(self):
        return self["items"]

    @property
    def receipt_sum(self):
        return self["receipt_sum"]
