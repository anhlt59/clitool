import pytest

from clitool.services import S3Service, SessionService

session = SessionService()
service = S3Service(session)

BUCKET_NAME = "cli-testing"


@pytest.fixture
def cli_s3_bucket(s3_client):
    s3_client.create_bucket(Bucket=BUCKET_NAME)


def test_list_buckets(cli_s3_bucket):
    buckets = service.bucket.list()
    assert len(buckets.items) == 1
    assert buckets.items[0].name == BUCKET_NAME


def test_put_objects(cli_s3_bucket, s3_client):
    key = "test.txt"
    s3_client.put_object(Bucket=BUCKET_NAME, Key=key, Body=b"test")

    objects = service.object.list(BUCKET_NAME)
    assert len(objects.items) == 1
    assert objects.items[0].key == key
