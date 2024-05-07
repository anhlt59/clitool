import os

import click
from click import Command
from click_shell import Shell
from rich.tree import Tree

from clitool.console import console
from clitool.constants import AWS_REGIONS, BASE_DIR
from clitool.types.session import ProfileTable


def list_commands(command: Shell, parent: Tree | None = None, max_depth: int = 0):
    if parent is None:
        parent = Tree(command.name, style="bold green")

    for name, sub_command in command.commands.items():
        if name == "tree" or name == "config":
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


def validate_file(ctx, param, value: str = "", help_text: str = "Please enter a file path") -> str:
    path = value.strip(" \n")
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


def validate_profile(ctx=None, param=None, value="") -> str:
    value = value.strip(" \n")
    profiles = ctx.obj["session"].list_profiles()
    profile_names = [profile.name for profile in profiles.items]

    # # if profile_name is not None, check if it exists in the list of profiles
    # # else try to get the profile from cache
    # if name == "":
    #     if cached_profile := ctx.obj.get("profile"):
    #         return validate_profile(ctx, param, cached_profile.arn)
    if value in profile_names:
        return value
    else:
        console.clear()
        console.log(f"Profile(name='{value}') not found", style="yellow")

    # if profile is not found, prompt the user to choose a profile
    profile_table = ProfileTable(items=profiles.items, columns=["name", "region"])
    console.print_table(profile_table)
    return validate_profile(ctx, param, click.prompt("Please choice a profile name"))


def validate_region(ctx=None, param=None, value="") -> str:
    value = value.strip(" \n")
    if value in AWS_REGIONS:
        return value

    console.clear()
    console.log(f"Region '{value}' is invalid", style="yellow")
    # if region is invalid, prompt the user to choose a profile
    return validate_profile(ctx, param, click.prompt("Please enter a region name"))


# CLI commands ---------------------------------------------------------------
@click.command()
@click.option("-d", "--depth", "max_depth", default=0, help="Depth of the tree")
@click.pass_context
def tree(ctx, max_depth: int):
    root_command = ctx.parent.command
    _tree = list_commands(root_command, max_depth=max_depth)
    console.print(_tree)


@click.command()
@click.option("-p", "--profile", "profile_name", default="", help="AWS profile")
@click.option("-r", "--region", "region_name", default="", help="AWS region")
@click.pass_context
def config(ctx, region_name: str, profile_name: str):
    session = ctx.obj["session"]
    # validate profile and region
    if profile_name == "" and region_name == "":
        console.print(f"Current profile: {session.profile.extract('name', 'region')}")
        console.print(
            "To change the profile or region, use the following options:\n",
            "  -p, --profile TEXT  AWS profile\n",
            "  -r, --region  TEXT  AWS region",
            style="yellow",
        )
        return None
    if profile_name:
        profile_name = validate_profile(ctx, None, profile_name)
        if session.profile.name == profile_name and session.profile.region == region_name:
            console.print(f"Already in profile [b]{profile_name}[/b], region [b]{region_name}[/b]", style="yellow")
            return None
    if region_name:
        region_name = validate_region(ctx, None, region_name)
        if profile_name == "" and session.profile.region == region_name:
            console.print(f"Already in region [b]{region_name}[/b]", style="yellow")
            return None

    # switch profile or region
    if profile_name:
        if region_name:
            session.switch_profile(profile_name, region_name)
            console.print(f"✅ Switched to profile [b]{profile_name}[/b], region [b]{region_name}[/b]")
        else:
            session.switch_profile(profile_name)
            console.print(f"✅ Switched to profile [b]{profile_name}[/b]")
    elif region_name:
        session.change_region(region_name)
        console.print(f"✅ Switched to region [b]{region_name}[/b]")
