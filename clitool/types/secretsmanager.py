from dataclasses import dataclass
from datetime import datetime

from clitool.types import CliItem, CliItems, CliTable


@dataclass
class SecretKey(CliItem):
    name: str
    arn: str
    version_id: str = ""
    secret_string: str = ""
    created_date: datetime | None = None


@dataclass
class SecretFilterCondition:
    prefix_name: list[str] | None = None
    prefix_tag_key: list[str] | None = None
    prefix_tag_value: list[str] | None = None
    all_attributes: list[str] | None = None

    @property
    def filters(self):
        filters = []
        if self.prefix_name:
            filters.append({"Key": "name", "Values": [self.prefix_name]})
        if self.prefix_tag_key:
            filters.append({"Key": "tag-key", "Values": [self.prefix_tag_key]})
        if self.prefix_tag_value:
            filters.append({"Key": "tag-value", "Values": [self.prefix_tag_value]})
        if self.all_attributes:
            filters.append({"Key": "all", "Values": [self.all_attributes]})
        return filters


class SecretKeys(CliItems):
    item_class = SecretKey


class SecretTable(CliTable):
    item_class = SecretKey
