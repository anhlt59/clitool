from click_shell import shell

from .custom import cli as custom_cli
from .policy import cli as policy_cli
from .role import cli as role_cli


@shell("iam", prompt="AWS ❯ IAM ❯ ")
def cli():
    """AWS IAM."""
    pass


cli.add_command(role_cli)
cli.add_command(policy_cli)
cli.add_command(custom_cli)

__all__ = ["cli"]
