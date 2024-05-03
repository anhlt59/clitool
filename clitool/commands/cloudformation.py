import time

import click
from click_shell import shell
from rich.live import Live

from clitool.commands.base import validate_required_value
from clitool.console import console
from clitool.services import CloudFormationService, SessionService
from clitool.types.cloudformation import CfnStackTable

session = SessionService()
cloudformation = CloudFormationService(session)


# CLI commands ---------------------------------------------------------------
@shell("cfn", prompt="AWS ❯ CloudFormation ❯ ")
def cli():
    """AWS CloudFormation."""
    pass


@cli.command("list")
@click.option("-p", "--prefix", help="Stack prefix", type=str, default=None)
def list_(prefix: str):
    """List cloudformation stacks."""
    with console.status("Listing cloudformation stack ...", spinner="dots"):
        try:
            stacks = cloudformation.list_stacks(prefix=prefix)
        except Exception as e:
            console.log(f"Failed to get stack: {e}", style="red")
        else:
            stack_table = CfnStackTable(items=stacks.items, columns=["name", "status", "reason", "last_updated_time"])
            console.print_table(stack_table)


@cli.command()
@click.argument("name", default="", required=False, callback=validate_required_value)
def get(name: str):
    """Describe a cloudformation stack."""
    with console.status(f"Getting [b][cyan]{name}[/cyan][/b] stack ...", spinner="dots"):
        try:
            stack = cloudformation.get_stack(name)
        except Exception as e:
            console.log(f"Failed to get stack: {e}", style="red")
        else:
            console.print(stack.extract())


@cli.command()
@click.argument("name", default="", required=False, callback=validate_required_value)
@click.option("-t", "--timeout", help="Monitoring timeout", type=int, default=600)
def monitor(name: str, timeout: int):
    """Monitor a cloudformation stack."""
    with console.status(
        f"Monitoring [b][cyan]{name}[/cyan][/b] stack. [white]Press Ctrl+C to stop[/white]", spinner="dots"
    ):
        with Live(CfnStackTable().table, refresh_per_second=0.3) as live:
            while timeout > 0:
                try:
                    stack = cloudformation.get_stack(name)
                except KeyboardInterrupt:
                    console.log("Stopped monitoring stack", style="yellow")
                except Exception as e:
                    console.log(f"Failed to get stack: {e}", style="error")
                else:
                    live.update(CfnStackTable(stack).table)
                    time.sleep(1)
                    timeout -= 1
            else:
                raise click.Abort("Timed out!!!")
