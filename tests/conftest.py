import boto3
import pytest
from moto import mock_aws

REGION = "us-east-1"
STAGE = "testing"


# service clients -------------------------------------------------------------
@pytest.fixture
def moto_session():
    with mock_aws():
        yield boto3.Session()


@pytest.fixture
def sts_client():
    with mock_aws():
        yield boto3.client("sts", region_name=REGION)


@pytest.fixture
def iam_client():
    with mock_aws():
        yield boto3.client("iam", region_name=REGION)


@pytest.fixture
def s3_client():
    with mock_aws():
        yield boto3.client("s3", region_name=REGION)


@pytest.fixture
def cfn_client():
    with mock_aws():
        yield boto3.client("cloudformation", region_name=REGION)


@pytest.fixture
def secretsmanager_client():
    with mock_aws():
        yield boto3.client("secretsmanager", region_name=REGION)


# resources -------------------------------------------------------------------
@pytest.fixture
def cli_user(iam_client):
    response = iam_client.create_user(Path="/developer/", UserName="anhlt")
    return response["User"]


@pytest.fixture
def cli_role(iam_client):
    response = iam_client.create_role(
        Path="/cli/testing/",
        RoleName="BackendDeveloper",
        AssumeRolePolicyDocument="""
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"Service": "s3.amazonaws.com"}
                    },
                    "Action": "sts:AssumeRole"
                ]
            }
        """,
    )
    return response["Role"]


@pytest.fixture
def mfa_device(iam_client, cli_user):
    response = iam_client.create_virtual_mfa_device(Path="/developer/", VirtualMFADeviceName="VirtualAnhlt")
    return response["VirtualMFADevice"]
