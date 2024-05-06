import time

import click
from click_shell import shell
from rich.live import Live
from rich.text import Text

from clitool.commands.base import validate_file, validate_required_value
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
def list_stacks(prefix: str):
    """List cloudformation stacks."""
    with console.status("Listing cloudformation stack ...", spinner="dots"):
        try:
            stacks = cloudformation.list_stacks(prefix=prefix)
        except Exception as e:
            console.log(f"🔥 Failed to list stacks: {e}", style="red")
        else:
            stack_table = CfnStackTable(items=stacks.items, columns=["name", "status", "reason", "last_updated_time"])
            console.print_table(stack_table)


@cli.command()
@click.argument("name", default="", required=False, callback=validate_required_value)
def get_stack(name: str):
    """Describe a cloudformation stack."""
    with console.status(f"Getting [b][cyan]{name}[/cyan][/b] stack ...", spinner="dots"):
        try:
            stack = cloudformation.get_stack(name)
        except Exception as e:
            console.log(f"🔥 Failed to get stack: {e}", style="red")
        else:
            console.print(stack.extract())


@cli.command()
@click.argument("name", default="", required=False, callback=validate_required_value)
@click.option("-t", "--timeout", help="Monitoring timeout", type=int, default=600)
def monitor_stack(name: str, timeout: int):
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
                    console.log(f"🔥 Failed to get stack: {e}", style="error")
                else:
                    live.update(CfnStackTable(stack).table)
                    time.sleep(1)
                    timeout -= 1
            else:
                raise click.Abort("🕙 Timed out!!!")


@cli.command()
@click.argument("path", default="", required=False, callback=validate_file)
def validate_template(path: str):
    """Validate cloudformation template."""
    with console.status(f"Validating [b][cyan]{path}[/cyan][/b] template ...", spinner="dots"):
        try:
            errors = cloudformation.validate_template(path)
        except Exception as e:
            console.log(f"🔥 Failed to validate template: {e}", style="red")
        else:
            if not errors:
                console.print("🎉 Template is valid", style="bold green")
            else:
                text = Text("📋 Template validation result:", style="bold white")
                for error in errors:
                    if error.rule.severity == "error":
                        text.append(f"\n{error}", style="red")
                    elif error.rule.severity == "warning":
                        text.append(f"\n{error}", style="yellow")
                    else:
                        text.append(f"\n{error}", style="white")
                console.print(text)
