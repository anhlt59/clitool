from clitool.services.base import AwsService
from clitool.types.base import Tag
from clitool.types.secrets_manager import SecretFilterCondition, SecretKey, SecretKeys


class SecretsManagerService(AwsService):
    @property
    def client(self):
        return self.session.client("secretsmanager")

    def list_secrets(self, filter_: SecretFilterCondition | None = None) -> SecretKeys:
        secret_keys = SecretKeys()
        response = self.client.list_secrets(Filters=filter_.filters)
        for secret in response["SecretList"]:
            secret_keys.append(
                SecretKey(
                    name=secret["Name"],
                    arn=secret["ARN"],
                    created_date=secret.get("CreatedDate"),
                    tags=[Tag(key=tag["Key"], value=tag["Value"]) for tag in secret.get("Tags", [])],
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
        )

    def create_secret(self, name: str, secret_string: str) -> SecretKey:
        response = self.client.create_secret(Name=name, SecretString=secret_string)
        return SecretKey(
            name=response["Name"],
            arn=response["ARN"],
            version_id=response["VersionId"],
        )

    def update_secret(self, secret_id: str, secret_string: str) -> SecretKey:
        response = self.client.put_secret_value(SecretId=secret_id, SecretString=secret_string)
        return SecretKey(
            name=response["Name"],
            arn=response["ARN"],
            version_id=response["VersionId"],
        )
