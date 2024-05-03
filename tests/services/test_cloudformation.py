import os

import pytest

from clitool.services import CloudFormationService, SessionService
from tests import DUMMY_DIR

session = SessionService()
service = CloudFormationService(session)

STACK_NAME = "cli-testing"


@pytest.fixture
def cli_stack(cfn_client):
    with open(os.path.join(DUMMY_DIR, "cloudformation", "cfn-template.yaml"), "r") as f:
        template_body = f.read()
    cfn_client.create_stack(StackName=STACK_NAME, TemplateBody=template_body)


def test_list_stacks(cli_stack):
    stacks = service.list_stacks()
    assert len(stacks.items) == 1
    assert stacks.items[0].name == STACK_NAME


def test_get_stack(cli_stack):
    stack = service.get_stack(STACK_NAME)
    assert stack.name == STACK_NAME and stack.status == "CREATE_COMPLETE"


def test_validate_stack(cfn_client):
    template_path = os.path.join(DUMMY_DIR, "cloudformation", "cfn-template.yaml")
    errors = service.validate_template(template_path)
    assert len(errors) == 0

    template_path = os.path.join(DUMMY_DIR, "cloudformation", "sam-template.yaml")
    errors = service.validate_template(template_path)
    assert len(errors) == 0

    template_path = os.path.join(DUMMY_DIR, "cloudformation", "invalid-template.yaml")
    errors = service.validate_template(template_path)
    assert len(errors) > 0
