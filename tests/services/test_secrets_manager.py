import pytest

from clitool.services import SecretsManagerService, SessionService

session = SessionService()
service = SecretsManagerService(session)

SECRET_KEY = "cli/testing"


@pytest.fixture
def secret_key(secretsmanager_client):
    secretsmanager_client.create_secret(Name=SECRET_KEY, SecretString='{"foo": "bar"}')


def test_list_secrets(secretsmanager_client, secret_key):
    secrets = service.list_secrets()
    assert len(secrets.items) == 1
    assert secrets.items[0].name == SECRET_KEY


def test_create_secrets(secretsmanager_client):
    service.create_secret(SECRET_KEY, '{"foo": "bar"}')
    secret = service.get_secret(SECRET_KEY)
    assert secret.name == SECRET_KEY


def test_update_secrets(secretsmanager_client, secret_key):
    service.update_secret(SECRET_KEY, '{"foo": "baz"}')
    secret = service.get_secret(SECRET_KEY)
    assert secret.secret_string == '{"foo": "baz"}'


def test_delete_secrets(secretsmanager_client, secret_key):
    service.delete_secret(SECRET_KEY)
    secrets = service.list_secrets()
    assert len(secrets.items) == 1
    assert secrets.items[0].deleted_date is not None
