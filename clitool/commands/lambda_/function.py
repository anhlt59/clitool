import click
from click_shell import shell

from clitool.commands.base import validate_required_value
from clitool.console import console
from clitool.services import LambdaService, SessionService

from .base import validate_payload

session = SessionService()
lambda_ = LambdaService(session)


# CLI commands ---------------------------------------------------------------
@shell("function", prompt="AWS ❯ Lambda ❯ Function ❯ ")
def cli():
    pass


@cli.command("list")
@click.option("-f", "--filter", "name_filter", help="Filter by function name", type=str, default="")
def list_(name_filter: str):
    """List all Lambda functions in the account with optional name filter."""
    # with console.status("Listing Lambda functions ...", spinner="dots"):
    try:
        functions = lambda_.function.list(name_filter)
    except Exception as e:
        console.log(f"Failed to invoke lambda function: {e}", style="red")
    else:
        console.print(functions.extract())


@cli.command()
@click.option("-n", "--name", help="Function name", default="", callback=validate_required_value)
@click.option("-p", "--payload", help="Payload", default="", callback=validate_payload)
def invoke(name: str, payload: dict):
    """Invoke a lambda function."""
    with console.status(f"Invoking [b][cyan]{name}[/cyan][/b] lambda function ...", spinner="dots"):
        try:
            result = lambda_.function.invoke(name, payload)
        except Exception as e:
            console.log(f"Failed to invoke lambda function: {e}", style="red")
        else:
            console.print(result.extract())
