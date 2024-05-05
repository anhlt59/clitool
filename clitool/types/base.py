from abc import ABC
from dataclasses import asdict, dataclass
from datetime import date, datetime
from typing import Type, TypeVar

from clitool.constants import DATETIME_FORMAT


def json_serializer(obj_):
    if isinstance(obj_, datetime) or isinstance(obj_, date):
        return obj_.strftime(DATETIME_FORMAT)
    if isinstance(CliItem, obj_):
        return obj_.serialize()


@dataclass
class CliItem(ABC):
    def serialize(self):
        return asdict(self)

    @classmethod
    def deserialize(cls, data: dict) -> "CliItem":
        return cls(**data)

    def extract(self, *attrs_to_get) -> dict:
        data = self.serialize()
        if attrs_to_get:
            data = {key: data[key] for key in attrs_to_get}
        return data


CliItemT = TypeVar("CliItemT", bound=CliItem)


class CliItems(ABC):
    item_class: Type[CliItemT]
    items: list[CliItemT]
    max_items: int
    next_token: str | None

    def __init__(self, items: list[CliItemT] = None, max_items: int = 50, next_token: str | None = None):
        self.items = items or []
        self.max_items = max_items
        self.next_token = next_token

    def extract(self, *attrs_to_get) -> list[dict]:
        return [item.extract(*attrs_to_get) for item in self.items]

    def append(self, item: CliItemT):
        self.items.append(item)


@dataclass
class Tag:
    key: str
    value: str
