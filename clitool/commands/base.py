import os

import click
from click import Command
from click_shell import Shell
from rich.tree import Tree

from clitool.console import console
from clitool.constants import BASE_DIR


def list_commands(command: Shell, parent: Tree | None = None, max_depth: int = 0):
    if parent is None:
        parent = Tree(command.name, style="bold green")

    for name, sub_command in command.commands.items():
        if name == "tree":
            continue

        if isinstance(sub_command, Shell):
            child = parent.add(f"{name: <25} [italic white]{sub_command.help or ''}[/italic white]", style="green")
            if max_depth > 0:
                list_commands(sub_command, child, max_depth - 1)
        elif isinstance(sub_command, Command):
            parent.add(f"{name: <25} [italic white]{sub_command.help or ''}[/italic white]", style="cyan1")

    return parent


# Validators ------------------------------------------------------------------
def validate_required_value(ctx, param, value: str = "") -> str:
    value = value.strip(" \n")
    if value == "":
        if isinstance(param, click.Option) or isinstance(param, click.Parameter):
            click.echo(f"{param.param_type_name.capitalize()} '{param.human_readable_name}' is missing.")
            return validate_required_value(
                ctx, param, click.prompt(f"Please enter a '{param.human_readable_name}' value")
            )
        else:
            click.Abort(f"Parameter {param} is invalid")
    return value


def validate_file(ctx, param, path: str = "", help_text: str = "Please enter a file path") -> str:
    path = path.strip(" \n")
    if path == "":
        return validate_file(ctx, param, click.prompt(help_text))
    elif path.startswith("~"):
        path = os.path.expanduser(path)
    elif path.startswith(".") or path.startswith("/") is False:
        path = os.path.join(BASE_DIR, path)

    if not path or os.path.isfile(path) is False:
        click.echo(f"File '{path}' not found")
        return validate_file(ctx, param, click.prompt("Please enter a file path"))
    return path


# CLI commands ---------------------------------------------------------------
@click.command()
@click.option("-d", "--depth", "max_depth", default=0, help="Depth of the tree")
@click.pass_context
def tree(ctx, max_depth: int):
    root_command = ctx.parent.command
    _tree = list_commands(root_command, max_depth=max_depth)
    console.print(_tree)
