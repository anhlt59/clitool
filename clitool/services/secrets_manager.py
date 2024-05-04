from clitool.services.base import AwsService
from clitool.types.base import Tag
from clitool.types.secrets_manager import SecretFilterCondition, SecretKey, SecretKeys


class SecretsManagerService(AwsService):
    @property
    def client(self):
        return self.session.client("secretsmanager")

    def list_secrets(self, filter_: SecretFilterCondition | None = None) -> SecretKeys:
        secret_keys = SecretKeys()
        response = self.client.list_secrets(Filters=filter_.filters if filter_ else [])
        for item in response["SecretList"]:
            secret_keys.append(
                SecretKey(
                    name=item["Name"],
                    arn=item["ARN"],
                    created_date=item.get("CreatedDate"),
                    deleted_date=item.get("DeletedDate"),
                    tags=[Tag(key=tag["Key"], value=tag["Value"]) for tag in item.get("Tags", [])],
                )
            )
        return secret_keys

    def get_secret(self, secret_id: str) -> SecretKey:
        response = self.client.get_secret_value(SecretId=secret_id)
        return SecretKey(
            name=secret_id,
            arn=response["ARN"],
            secret_string=response["SecretString"],
            created_date=response.get("CreatedDate"),
            deleted_date=response.get("DeletedDate"),
            tags=[Tag(key=tag["Key"], value=tag["Value"]) for tag in response.get("Tags", [])],
        )

    def create_secret(self, name: str, secret_string: str) -> SecretKey:
        response = self.client.create_secret(Name=name, SecretString=secret_string)
        return SecretKey(
            name=response["Name"],
            arn=response["ARN"],
            version_id=response["VersionId"],
            created_date=response.get("CreatedDate"),
        )

    def update_secret(self, secret_id: str, secret_string: str) -> SecretKey:
        response = self.client.put_secret_value(SecretId=secret_id, SecretString=secret_string)
        return SecretKey(
            name=response["Name"],
            arn=response["ARN"],
            version_id=response["VersionId"],
            created_date=response.get("CreatedDate"),
        )

    def delete_secret(self, secret_id: str, recovery_window=30) -> SecretKey:
        response = self.client.delete_secret(SecretId=secret_id, RecoveryWindowInDays=recovery_window)
        return SecretKey(
            name=response["Name"],
            arn=response["ARN"],
            created_date=response.get("CreatedDate"),
            deleted_date=response.get("DeletedDate"),
        )
