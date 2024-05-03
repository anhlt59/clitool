from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Literal

from clitool.types import CliTable
from clitool.types.base import CliItem, CliItems

# fmt: off
CloudFormationStatus = Literal["CREATE_IN_PROGRESS", "CREATE_FAILED", "CREATE_COMPLETE", "ROLLBACK_IN_PROGRESS", "ROLLBACK_FAILED", "ROLLBACK_COMPLETE", "DELETE_IN_PROGRESS", "DELETE_FAILED", "DELETE_COMPLETE", "UPDATE_IN_PROGRESS", "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS", "UPDATE_COMPLETE", "UPDATE_FAILED", "UPDATE_ROLLBACK_IN_PROGRESS", "UPDATE_ROLLBACK_FAILED", "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS", "UPDATE_ROLLBACK_COMPLETE", "REVIEW_IN_PROGRESS", "IMPORT_IN_PROGRESS", "IMPORT_COMPLETE", "IMPORT_ROLLBACK_IN_PROGRESS", "IMPORT_ROLLBACK_FAILED", "IMPORT_ROLLBACK_COMPLETE"]  # noqa
# fmt: on


@dataclass
class CfnParameters:
    key: str
    value: str
    previous_value: str
    resolved_value: str


@dataclass
class CfnStack(CliItem):
    name: str
    id: str | None = None
    status: CloudFormationStatus | None = None
    reason: str | None = None
    parameters: list[CfnParameters] | None = None
    role_arn: str | None = None
    creation_time: datetime | None = None
    last_updated_time: datetime | None = None
    # deletion_time: datetime | None = None


class CfnStacks(CliItems):
    item_class = CfnStack


class CfnStackTable(CliTable):
    item_class = CfnStack

    def serialize_item(self, data: dict) -> Iterable[str]:
        if parameters := data.get("parameters"):
            data["parameters"] = "\n".join([f"{param['key']}={param['value']}" for param in parameters])
        return super().serialize_item(data)
