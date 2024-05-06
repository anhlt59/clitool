import click
from botocore.errorfactory import ClientError
from click_shell import shell

from clitool.commands.base import validate_required_value
from clitool.console import console
from clitool.services import SecretsManagerService, SessionService
from clitool.types.secrets_manager import SecretFilterCondition, SecretTable
from clitool.utils import rich_diff

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
        prefix_name=name,
        prefix_tag_key=tag_key,
        prefix_tag_value=tag_value,
        all_attributes=all_,
    )
    with console.status("Listing secret keys ...", spinner="dots"):
        try:
            secrets = secretsmanager.list_secrets(filter_)
        except Exception as e:
            console.log(f"Failed to get stack: {e}", style="red")
        else:
            secret_table = SecretTable(items=secrets.items, columns=["name", "arn", "created_date", "tags"])
            console.print_table(secret_table)


@cli.command()
@click.argument("secret_id", type=str, required=False, default="", callback=validate_required_value)
def get(secret_id: str):
    """Get a secretsmanager key."""
    with console.status(f"Getting [b][cyan]{secret_id}[/cyan][/b] key ...", spinner="dots"):
        try:
            secret = secretsmanager.get_secret(secret_id)
        except Exception as e:
            console.log(f"Failed to get stack: {e}", style="red")
        else:
            console.print(secret.extract())


@cli.command()
@click.argument("secret_id", type=str, required=False, default="", callback=validate_required_value)
@click.argument("secret_string", type=str, required=False, default="", callback=validate_required_value)
def upsert(secret_id: str, secret_string: str):
    """Create or update a secretsmanager key."""
    with console.status(f"Waiting for checking [b][cyan]{secret_id}[/cyan][/b] key ...", spinner="dots"):
        try:
            existing_secret = secretsmanager.get_secret(secret_id)
        except Exception as e:
            if isinstance(e, ClientError) and e.response["Error"]["Code"] == "ResourceNotFoundException":
                existing_secret = None
            else:
                console.log(f"Failed to create/update key: {e}", style="red")
                raise click.Abort()

    if existing_secret:
        if diff := rich_diff(existing_secret.secret_string, secret_string):
            console.print(diff)
            click.confirm(f"Do you want to update the secret {secret_id}?", abort=True, default=True)
            with console.status(f"Updating [b][cyan]{secret_id}[/cyan][/b] key ...", spinner="dots"):
                try:
                    secret = secretsmanager.update_secret(secret_id, secret_string)
                except Exception as e:
                    console.log(f"Failed to update key: {e}", style="red")
                else:
                    console.print(secret.extract(), f"Updated [b]{secret_id}[/b] successfully.")
        else:
            console.log("No changes detected.")

    else:
        click.confirm("Do you want to create a new secret?", abort=True, default=True)
        with console.status(f"Creating [b][cyan]{secret_id}[/cyan][/b] key ...", spinner="dots"):
            try:
                secret = secretsmanager.create_secret(secret_id, secret_string)
            except Exception as e:
                console.log(f"Failed to update key: {e}", style="red")
            else:
                console.print(secret.extract(), f"Created [b]{secret_id}[/b] successfully.")


@cli.command()
@click.argument("secret_id", type=str, required=False, default="", callback=validate_required_value)
def delete(secret_id: str):
    """Delete a secretsmanager key."""
    try:
        secret = secretsmanager.get_secret(secret_id)
    except Exception as e:
        console.log(f"Failed to get secret: {e}", style="red")
        raise click.Abort()
    console.print(secret.extract())

    click.confirm(f"Are you sure you want to delete the secret {secret_id}?", abort=True, default=False)
    with console.status(f"Deleting [b][cyan]{secret_id}[/cyan][/b] key ...", spinner="dots"):
        try:
            secretsmanager.delete_secret(secret_id)
        except Exception as e:
            console.log(f"Failed to delete key: {e}", style="red")
        else:
            console.print(f"Deleted [b]{secret_id}[/b] successfully.")
