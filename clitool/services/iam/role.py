from clitool.services.base import AwsService
from clitool.types.iam import Role, Roles


class IamRoleService(AwsService):
    @property
    def client(self):
        return self.session.client("iam")

    def get(self, arn: str, lazy=True) -> Role:
        pass

    def list(self, **kwargs) -> Roles:
        def _list_roles(**_kwargs):
            prefix = _kwargs.pop("PathPrefix", None)
            response = self.client.list_roles(**_kwargs)

            for item in response.get("Roles", []):
                if not prefix or f"role/{prefix}" in item.get("Arn"):
                    yield Role(
                        arn=item.get("Arn"),
                        profile=self.session.profile,
                    )
            if response.get("IsTruncated"):
                _kwargs.update(Marker=response.get("Marker"), PathPrefix=prefix)
                yield from self.list(**_kwargs)

        roles = Roles()
        for role in _list_roles(**kwargs):
            roles.append(role)
        return roles
