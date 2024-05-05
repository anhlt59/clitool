import json
import os

from clitool.console import console
from clitool.constants import CUSTOM_FILE
from clitool.services.base import AwsService
from clitool.types.iam import Role, Roles


class IamCustomService(AwsService):
    @property
    def client(self):
        return self.session.client("iam")

    def list(self, lazy=True) -> Roles:
        roles = Roles()
        if not os.path.exists(CUSTOM_FILE):
            return roles

        with open(CUSTOM_FILE) as f:
            data = json.load(f)

        if isinstance(data, dict) is False or "roles" not in data:
            console.log("Invalid 'roles' in custom.json", style="red")
            return roles

        for item in data.get("roles", []):
            profile = self.session.get_profile(item.get("profile"), lazy=lazy)
            roles.append(Role(arn=item.get("arn"), profile=profile))
        return roles

    def get(self, arn: str, lazy=True) -> Role:
        roles = self.list(lazy=lazy)
        for item in roles.items:
            if item.arn == arn:
                role = item
                break
        else:
            raise Exception(f"Role {arn} not found")
        return role
