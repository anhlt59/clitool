from dataclasses import dataclass, field
from datetime import datetime

from clitool.types import CliTable
from clitool.types.base import CliItem, CliItems


@dataclass
class EcrRepository(CliItem):
    name: str
    arn: str | None = None
    uri: str | None = None
    registry_id: str | None = None
    created_at: datetime | None = None


@dataclass
class EcrImage(CliItem):
    registry_id: str | None = None
    repository_name: str | None = None
    image_digest: str | None = None
    image_tags: list[str] = field(default_factory=lambda: [])
    image_size_in_bytes: int | None = None
    image_pushed_at: datetime | None = None
    last_pulled_at: datetime | None = None


class EcrRepositories(CliItems):
    item_class = EcrRepository


class EcrImages(CliItems):
    item_class = EcrImage


class EcrRepositoryTable(CliTable):
    item_class = EcrRepository


class EcrImageTable(CliTable):
    item_class = EcrImage
