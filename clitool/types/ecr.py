from dataclasses import dataclass
from datetime import datetime

from clitool.types import CliTable
from clitool.types.base import CliItem, CliItems


@dataclass
class EcrRepository(CliItem):
    name: str
    arn: str | None = None
    id: str | None = None
    uri: str | None = None
    created_at: datetime | None = None


class EcrRepositories(CliItems):
    item_class = EcrRepository


class EcrTable(CliTable):
    item_class = EcrRepository
