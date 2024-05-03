from dataclasses import dataclass
from datetime import datetime, timezone

from clitool.types import CliItem, CliItems, CliTable, CliTableSettings


@dataclass
class Credentials(CliItem):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str | None = None
    aws_expiration: datetime | None = None
    aws_arn: str | None = None

    def is_expired(self):
        if self.aws_expiration is None:
            return False
        return self.aws_expiration < datetime.now(timezone.utc)


@dataclass
class Profile(CliItem):
    credentials: Credentials
    name: str
    region: str
    user_id: str | None = None
    account: str | None = None
    arn: str | None = None

    def serialize(self):
        return {
            "name": self.name,
            "region": self.region,
            "user_id": self.user_id,
            "account": self.account,
            "arn": self.arn,
            "credentials": self.credentials.serialize(),
        }

    @classmethod
    def deserialize(cls, data: dict) -> "Profile":
        return cls(
            name=data.get("name"),
            region=data.get("region"),
            user_id=data.get("user_id"),
            account=data.get("account"),
            arn=data.get("arn"),
            credentials=Credentials.deserialize(data.get("credentials")),
        )


class Profiles(CliItems):
    item_class = Profile


class ProfileTable(CliTable):
    settings = CliTableSettings(
        column_styles={
            "name": {"header": "name", "justify": "left", "style": "green", "overflow": "fold"},
            "region": {"header": "region", "justify": "left", "style": "yellow", "overflow": "fold"},
            "user_id": {"header": "user_id", "justify": "left", "style": "cyan", "overflow": "fold"},
            "account": {"header": "account", "justify": "left", "style": "cyan1", "overflow": "fold"},
            "arn": {"header": "arn", "justify": "left", "style": "white", "overflow": "fold"},
        }
    )

    item_class = Profile


# Session interface
# class Session(Protocol):
#     profile: Profile
#
#     session: boto3.Session
#     client: Type[boto3.client]
#     resource: Type[boto3.resource]
#
#     def get_profile(self, name: str, lazy=True) -> Profile:
#         """Get an available profile by name."""
#
#     def list_profiles(self) -> list[Profile]:
#         """List all available profiles on your system."""
#
#     def switch_profile(self, name: str) -> Profile:
#         """Switch to a profile."""
#
#     def set_credentials(self, credentials: Credentials) -> Profile:
#         """Set credentials for a profile."""
#
#     def assume_role(self, arn: str) -> Credentials:
#         """Assume a IAM role."""
#
#     def get_session_token(self, arn: str, mfa_token: str) -> Credentials:
#         """Get a session token."""
#
#     def store_aws_config_file(self, profile: Profile, name: str):
#         """Store the profile in the AWS config file."""
