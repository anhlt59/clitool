from dataclasses import dataclass
from datetime import datetime

from clitool.types import CliItem, CliItems, CliTable
from clitool.types.base import Tag


@dataclass
class SecretKey(CliItem):
    name: str
    arn: str | None = None
    version_id: str | None = None
    secret_string: str | None = None
    tags: list[Tag] | None = None
    created_date: datetime | None = None
    deleted_date: datetime | None = None


@dataclass
class SecretFilterCondition:
    prefix_name: str | None = None
    prefix_tag_key: str | None = None
    prefix_tag_value: str | None = None
    all_attributes: str | None = None

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
