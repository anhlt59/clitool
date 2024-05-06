import click
from click_shell import shell

from clitool.console import console
from clitool.services import DynamoDBService, SessionService
from clitool.types.dynamodb import DynamoDBCliTable

session = SessionService()
dynamodb = DynamoDBService(session)


# CLI commands ---------------------------------------------------------------
@shell("dynamodb", prompt="AWS ❯ DynamoDB ❯ ")
def cli():
    """AWS DynamoDB."""
    pass


@cli.command("list")
@click.option("-p", "--prefix", help="Name prefix", type=str, default="")
def list_(prefix: str):
    """List dynamodb tables."""
    with console.status("Listing dynamodb tables ...", spinner="dots"):
        try:
            tables = dynamodb.list(prefix)
        except Exception as e:
            console.log(f"🔥 Failed to list dynamodb tables: {e}", style="red")
        else:
            cli_table = DynamoDBCliTable(items=tables.items)
            console.print_table(cli_table)
