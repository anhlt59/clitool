from dataclasses import dataclass

from clitool.types import CliItem, CliItems, CliTable, CliTableSettings
from clitool.types.session import Profile


@dataclass
class Role(CliItem):
    arn: str
    profile: Profile

    def serialize(self):
        return {"arn": self.arn, "profile": self.profile.serialize()}

    @classmethod
    def deserialize(cls, data: dict) -> "Role":
        return cls(
            arn=data.get("arn"),
            profile=Profile.deserialize(data.get("profile")),
        )

    def extract(self, *attrs_to_get) -> dict:
        data = super().extract()

        if attrs_to_get:
            filtered_data = {}
            profile = {}
            for key in ["name", "region", "user_id", "account", "arn", "credentials"]:
                if f"profile.{key}" in attrs_to_get:
                    profile[key] = data["profile"][key]
            if "arn" in attrs_to_get:
                filtered_data["arn"] = data["arn"]
            if profile:
                filtered_data["profile"] = profile
            return filtered_data

        return data


class Roles(CliItems):
    item_class = Role


class RoleTable(CliTable):
    item_class = Role

    settings = CliTableSettings(
        column_styles={
            "arn": {"header": "arn", "justify": "left", "style": "green", "overflow": "fold"},
            "profile.name": {"header": "profile.name", "justify": "left", "style": "yellow", "overflow": "fold"},
            "profile.region": {"header": "profile.region", "justify": "left", "style": "cyan", "overflow": "fold"},
            "profile.account": {"header": "profile.account", "justify": "left", "style": "cyan1", "overflow": "fold"},
            "profile.arn": {"header": "profile.arn", "justify": "left", "style": "white", "overflow": "fold"},
        }
    )

    def extract_item(self, item: CliItem, *attrs_to_get: str) -> dict:
        data = item.extract()
        data = {
            "arn": data["arn"],
            "profile.name": data["profile"]["name"],
            "profile.region": data["profile"]["region"],
            "profile.account": data["profile"]["account"],
            "profile.arn": data["profile"]["arn"],
        }
        if attrs_to_get:
            return {key: data[key] for key in attrs_to_get}
        return data
