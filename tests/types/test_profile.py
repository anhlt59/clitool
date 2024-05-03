from datetime import UTC, datetime, timedelta

import pytest

from clitool.types.session import Credentials, Profile


@pytest.fixture
def credentials():
    return Credentials(
        aws_access_key_id="AKIA1234567890",
        aws_secret_access_key="1234567890",
        aws_session_token=None,
        aws_expiration=None,
        aws_arn="arn:aws:iam::1234567890:user/test",
    )


def test_credentials(credentials):
    assert credentials.is_expired() is False
    credentials.aws_expiration = datetime.now(UTC) - timedelta(days=1)
    assert credentials.is_expired() is True
    credentials.aws_expiration = datetime.now(UTC) + timedelta(days=1)
    assert credentials.is_expired() is False


def test_profile(credentials):
    profile = Profile(
        name="testing",
        region="us-east-1",
        credentials=credentials,
    )
    data = profile.serialize()
    bk_profile = Profile.deserialize(data)

    assert bk_profile.name == profile.name
    assert bk_profile.region == profile.region
    assert bk_profile.credentials.aws_access_key_id == profile.credentials.aws_access_key_id
    assert bk_profile.credentials.aws_secret_access_key == profile.credentials.aws_secret_access_key
    assert bk_profile.credentials.aws_session_token == profile.credentials.aws_session_token
    assert bk_profile.credentials.aws_arn == profile.credentials.aws_arn
    assert bk_profile.credentials.aws_expiration == profile.credentials.aws_expiration
