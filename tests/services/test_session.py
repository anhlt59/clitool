from datetime import UTC, datetime

import pytest

from clitool.services import SessionService

session = SessionService()


def test_list_profiles(moto_session):
    profiles = session.list_profiles()
    assert len(profiles.items) == 2


def test_switch_profile(moto_session):
    profile = session.get_profile()
    assert profile.name == "default"
    profile = session.switch_profile("testing")
    assert profile.name == "testing"


def test_assume_role(cli_role):
    arn = cli_role["Arn"]
    credentials = session.assume_role(arn)
    assert credentials.aws_arn == arn
    assert credentials.aws_expiration > datetime.now(UTC)


def test_get_session_token(mfa_device):
    serial_number = mfa_device["SerialNumber"]
    credentials = session.get_session_token(serial_number, "123456")
    assert credentials.aws_arn == serial_number
    assert credentials.aws_expiration > datetime.now(UTC)
