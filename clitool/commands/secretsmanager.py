import click
from click_shell import shell

from clitool.commands.base import validate_required_value
from clitool.console import console
from clitool.services import SecretsManagerService, SessionService
from clitool.types.secretsmanager import SecretFilterCondition, SecretTable

session = SessionService()
secretsmanager = SecretsManagerService(session)


# CLI commands ---------------------------------------------------------------
@shell("secrets", prompt="AWS ❯ SecretsManager ❯ ")
def cli():
    """AWS SecretsManager."""
    pass


@cli.command("list")
@click.option("-n", "--name", help="Name prefix, case-sensitive", type=str, default="")
@click.option("--tag-key", help="Tag key prefix, case-sensitive", type=str, default="")
@click.option("--tag-value", help="Tag value prefix, case-sensitive", type=str, default="")
@click.option("--all", "all_", help="Prefix for all attributes, case-sensitive", type=str, default="")
def list_(name: str, tag_key: str, tag_value: str, all_: str):
    """List secret keys."""
    filter_ = SecretFilterCondition(
        prefix_name=[name] if name else None,
        prefix_tag_key=[tag_key] if tag_key else None,
        prefix_tag_value=[tag_value] if tag_value else None,
        all_attributes=[all_] if all_ else None,
    )
    with console.status("Listing secret keys ...", spinner="dots"):
        try:
            secrets = secretsmanager.list(filter_)
        except Exception as e:
            console.log(f"Failed to get stack: {e}", style="red")
        else:
            secret_table = SecretTable(items=secrets.items, columns=["name", "arn", "created_date"])
            console.print_table(secret_table)


@cli.command()
@click.argument("secret_id", type=str, required=False, default="", callback=validate_required_value)
def get(secret_id: str):
    """Get a secretsmanager keys."""
    with console.status(f"Getting [b][cyan]{secret_id}[/cyan][/b] key ...", spinner="dots"):
        try:
            secret = secretsmanager.get(secret_id)
        except Exception as e:
            console.log(f"Failed to get stack: {e}", style="red")
        else:
            console.print(secret.extract())
