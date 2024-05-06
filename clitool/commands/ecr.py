import click
from click_shell import shell

from clitool.commands.base import validate_required_value
from clitool.console import console
from clitool.services import EcrService, SessionService
from clitool.types.ecr import EcrImageTable, EcrRepositoryTable

session = SessionService()
ecr = EcrService(session)


# CLI commands ---------------------------------------------------------------
@shell("ecr", prompt="AWS ❯ ECR ❯ ")
def cli():
    """AWS ECR."""
    pass


@cli.command()
@click.option("-p", "--prefix", help="Name prefix", type=str, default="")
def list_repositories(prefix: str):
    """List ECR repositories."""
    with console.status("Listing ECR repositories ...", spinner="dots"):
        try:
            repositories = ecr.list_repositories(prefix)
        except Exception as e:
            console.log(f"🔥 Failed to list ECR repository: {e}", style="red")
        else:
            cli_table = EcrRepositoryTable(items=repositories.items)
            console.print_table(cli_table)


@cli.command()
@click.argument("repository_name", type=str, default="", callback=validate_required_value)
def list_images(repository_name: str):
    """List ECR images for a repository."""
    with console.status(f"Listing ECR images for repository '{repository_name}' ...", spinner="dots"):
        try:
            images = ecr.list_images(repository_name)
        except Exception as e:
            console.log(f"🔥 Failed to list ECR images: {e}", style="red")
        else:
            cli_table = EcrImageTable(items=images.items)
            console.print_table(cli_table)


@cli.command()
@click.argument("repository_name", type=str, default="", callback=validate_required_value)
def create_repository(repository_name: str):
    """Create an ECR repository."""
    click.confirm(f"Are you sure you want to create ECR repository '{repository_name}'?", abort=True)
    with console.status(f"Creating ECR repository '{repository_name}' ...", spinner="dots"):
        try:
            repository = ecr.create_repository(repository_name)
        except Exception as e:
            console.log(f"🔥 Failed to create ECR repository: {e}", style="red")
        else:
            console.print(repository, "🚀 Done!", style="green")
