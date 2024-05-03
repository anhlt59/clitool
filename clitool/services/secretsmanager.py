from clitool.services.base import AwsService
from clitool.types.secretsmanager import SecretFilterCondition, SecretKey, SecretKeys


class SecretsManagerService(AwsService):
    @property
    def client(self):
        return self.session.client("secretsmanager")

    def list(self, filter_: SecretFilterCondition | None = None) -> SecretKeys:
        secret_keys = SecretKeys()
        response = self.client.list_secrets(Filters=filter_.filters)
        for secret in response["SecretList"]:
            secret_keys.append(
                SecretKey(
                    name=secret["Name"],
                    arn=secret["ARN"],
                    created_date=secret.get("CreatedDate"),
                )
            )
        return secret_keys

    def get(self, secret_id: str) -> SecretKey:
        response = self.client.get_secret_value(SecretId=secret_id)
        return SecretKey(
            name=secret_id,
            arn=response["ARN"],
            secret_string=response["SecretString"],
            created_date=response.get("CreatedDate"),
        )
