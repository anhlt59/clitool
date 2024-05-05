from copy import deepcopy
from dataclasses import dataclass, field, fields
from datetime import date, datetime
from typing import Iterable, Type

from rich import box
from rich.table import Table

from clitool.constants import DATETIME_FORMAT

from .base import CliItem


@dataclass
class CliTableSettings:
    table_style: dict = field(default_factory=lambda: {})
    column_styles: dict = field(default_factory=lambda: {})
    columns: list[str] = field(default_factory=lambda: [])
    # Default settings
    default_column_style: dict = field(
        default_factory=lambda: {"justify": "left", "style": "green", "overflow": "fold"}
    )
    default_table_style: dict = field(
        default_factory=lambda: {"box": box.SIMPLE, "expand": False, "safe_box": True, "style": "cyan1"}
    )


class CliTableMeta(type):
    settings = CliTableSettings()

    def __new__(mcs, clsname, bases, methods):
        # update the default settings with the inherited classes
        if (settings := methods.get("settings")) is None:
            settings = mcs.settings
        methods["settings"] = settings = deepcopy(settings)

        if (item_class := methods.get("item_class")) is not None:
            # set default table style
            if hasattr(settings, "table_style") is False or len(settings.table_style) == 0:
                settings.table_style = deepcopy(mcs.settings.default_table_style)
            # set default column styles
            if hasattr(settings, "column_styles") is False or len(settings.column_styles) == 0:
                settings.column_styles = {}
                for column in fields(item_class):
                    style = deepcopy(settings.default_column_style)
                    style["header"] = column.name
                    settings.column_styles[column.name] = style
            if hasattr(settings, "columns") is False or len(settings.columns) == 0:
                settings.columns = list(settings.column_styles.keys())
        return type.__new__(mcs, clsname, bases, methods)


class CliTable(metaclass=CliTableMeta):
    item_class: Type[CliItem]
    table: Table
    settings: CliTableSettings

    def __init__(self, item: CliItem | None = None, items: Iterable[CliItem] = None, columns: list[str] | None = None):
        self.settings = self.update_settings(columns)
        self.table = self.create_table(self.settings.table_style, self.settings.column_styles)
        if item:
            self.add_item(item)
        if items:
            self.add_items(items)

    @classmethod
    def update_settings(cls, columns: list[str] | None = None) -> CliTableSettings:
        settings = deepcopy(cls.settings)
        if columns:
            settings.columns = columns
            settings.column_styles = {column: settings.column_styles[column] for column in columns}
        return settings

    @classmethod
    def create_table(cls, table_style: dict, column_styles: dict) -> Table:
        table = Table(**table_style)
        for column in column_styles.values():
            table.add_column(**column)
        return table

    def extract_item(self, item: CliItem, *attrs_to_get: str) -> dict:
        return item.extract(*attrs_to_get)

    def serialize_item(self, data: dict) -> Iterable[str]:
        for column in self.settings.columns:
            item = data.get(column)
            if item is None:
                yield ""
            elif isinstance(item, datetime) or isinstance(item, date):
                yield item.strftime(DATETIME_FORMAT)
            elif isinstance(item, CliItem):
                yield item.extract()
            else:
                yield str(item)

    def add_item(self, item: CliItem) -> Table:
        data = self.extract_item(item)
        serialized_data = self.serialize_item(data)
        self.table.add_row(*serialized_data)
        return self.table

    def add_items(self, items: Iterable[CliItem]) -> Table:
        for item in items:
            self.add_item(item)
        return self.table
