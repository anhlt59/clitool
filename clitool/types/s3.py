from dataclasses import dataclass
from datetime import datetime

from clitool.types import CliItem, CliItems, CliTable


@dataclass
class S3Bucket(CliItem):
    name: str
    creation_date: datetime | None = None


@dataclass
class S3Object(CliItem):
    key: str
    bucket: S3Bucket


class S3Buckets(CliItems):
    item_class = S3Bucket


class S3Objects(CliItems):
    item_class = S3Object


class S3BucketTable(CliTable):
    item_class = S3Bucket


class S3ObjectTable(CliTable):
    item_class = S3Object
