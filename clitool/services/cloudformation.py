from typing import Iterable

from cfnlint.api import lint_all

from clitool.services.base import AwsService
from clitool.types.cloudformation import CfnParameters, CfnStack, CfnStacks

AVAILABLE_STATUSES = (
    "CREATE_COMPLETE",
    "UPDATE_COMPLETE",
    "UPDATE_ROLLBACK_COMPLETE",
    "ROLLBACK_COMPLETE",
    "ROLLBACK_FAILED",
    "UPDATE_ROLLBACK_FAILED",
    "CREATE_IN_PROGRESS",
    "ROLLBACK_IN_PROGRESS",
    "DELETE_IN_PROGRESS",
    "UPDATE_IN_PROGRESS",
    "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS",
    "UPDATE_ROLLBACK_IN_PROGRESS",
    "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS",
    "REVIEW_IN_PROGRESS",
)


class CloudFormationService(AwsService):
    @property
    def client(self):
        return self.session.client("cloudformation")

    def list_stacks(self, prefix: str | None = None, status_filter: Iterable[str] = AVAILABLE_STATUSES) -> CfnStacks:
        stacks = CfnStacks()
        response = self.client.list_stacks(StackStatusFilter=status_filter)

        for item in response.get("StackSummaries", []):
            if prefix and not item.get("StackName").startswith(prefix):
                continue
            stacks.append(
                CfnStack(
                    id=item.get("StackId"),
                    name=item.get("StackName"),
                    status=item.get("StackStatus"),
                    reason=item.get("StackStatusReason"),
                    last_updated_time=item.get("LastUpdatedTime"),
                )
            )
        return stacks

    def get_stack(self, stack_name: str = None):
        response = self.client.describe_stacks(StackName=stack_name)
        if stacks := response["Stacks"]:
            data = stacks[0]

            stack = CfnStack(
                id=data.get("StackId"),
                name=data.get("StackName"),
                status=data.get("StackStatus"),
                reason=data.get("StackStatusReason"),
                role_arn=data.get("RoleARN"),
                creation_time=data.get("CreationTime"),
                last_updated_time=data.get("LastUpdatedTime"),
                parameters=[],
            )
            for param in data.get("Parameters", []):
                stack.parameters.append(
                    CfnParameters(
                        key=param.get("ParameterKey"),
                        value=param.get("ParameterValue"),
                        previous_value=param.get("UsePreviousValue"),
                        resolved_value=param.get("ResolvedValue"),
                    )
                )
            return stack
        raise Exception(f"Stack {stack_name} not found")

    def validate_template(self, template_path: str) -> list:
        with open(template_path, "r") as file:
            template = file.read()
        return lint_all(template)
