from dataclasses import dataclass

from clitool.types import CliTable
from clitool.types.base import CliItem, CliItems


@dataclass
class ProvisionedThroughput:
    read_capacity_units: int
    write_capacity_units: int


@dataclass
class KeySchema:
    attribute_name: str
    key_type: str


@dataclass
class LocalSecondaryIndex:
    index_name: str
    key_schema: list[KeySchema]
    projection: dict | None = None
    index_size_bytes: int | None = None
    item_count: int | None = None


@dataclass
class GlobalSecondaryIndex:
    index_name: str
    key_schema: list[KeySchema]
    projection: dict | None = None
    index_status: str | None = None
    index_size_bytes: int | None = None
    item_count: int | None = None
    provisioned_throughput: ProvisionedThroughput | None = None


@dataclass
class DynamoDBTable(CliItem):
    name: str
    arn: str | None = None
    status: str | None = None
    creation_date_time: str | None = None
    item_count: int | None = None
    size_bytes: int | None = None
    billing_mode: str | None = None
    local_secondary_indexes: list[LocalSecondaryIndex] | None = None
    global_secondary_indexes: list[GlobalSecondaryIndex] | None = None
    provisioned_throughput: ProvisionedThroughput | None = None


class DynamoDBTables(CliItems):
    item_class = DynamoDBTable


class DynamoDBCliTable(CliTable):
    item_class = DynamoDBTable
