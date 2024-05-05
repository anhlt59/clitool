import click
from click_shell import shell

from clitool.console import console
from clitool.services import EcrService, SessionService
from clitool.types.ecr import EcrTable

session = SessionService()
ecr = EcrService(session)


# CLI commands ---------------------------------------------------------------
@shell("ecr", prompt="AWS ❯ ECR ❯ ")
def cli():
    """AWS ECR."""
    pass


@cli.command("list")
@click.option("-p", "--prefix", help="Name prefix", type=str, default="")
def list_(prefix: str):
    """List ECR repositories."""
    with console.status("Listing ECR repositories ...", spinner="dots"):
        try:
            repos = ecr.list_repos(prefix)
        except Exception as e:
            console.log(f"Failed to get dynamodb tables: {e}", style="red")
        else:
            cli_table = EcrTable(items=repos.items, columns=["name", "arn", "uri"])
            console.print_table(cli_table)
