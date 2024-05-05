import re

import click
from click_shell import shell

from clitool.cache import cache
from clitool.console import console
from clitool.constants import AWS_DEFAULT_SESSION_PROFILE
from clitool.services import IamService, SessionService
from clitool.types.iam import RoleTable

MFA_ARN_PATTERN = r"(^arn:aws:iam::\d+:mfa/[\w\-_]+$)|(^\d{6,}$)"

session = SessionService()
iam = IamService(session)


# Validators ------------------------------------------------------------------
def validate_custom_role(ctx, param, arn: str = "") -> str:
    arn = arn.strip(" \n")
    available_roles = iam.custom.list()
    role_arns = [role.arn for role in available_roles.items]

    # if value is not None, check if it exists in the list of roles
    # else try to get the default role from cache
    if arn is None:
        if cached_role := ctx.obj.get("role"):
            return validate_custom_role(ctx, param, cached_role.arn)
    elif arn in role_arns:
        return arn
    else:
        console.clear()
        console.log(f"RoleArn(arn={arn}) not found", style="yellow")

    # if cache is empty or role is not found, prompt the user to choose a role
    role_table = RoleTable(items=available_roles.items, columns=["arn", "profile.name", "profile.region"])
    console.print_table(role_table)
    return validate_custom_role(ctx, param, click.prompt("Please choice a role arn"))


# CLI commands ---------------------------------------------------------------
@shell("custom", prompt="AWS ❯ IAM ❯ CustomRole ❯ ")
def cli():
    pass


@cli.command()
@click.argument("arn", required=False, default="", callback=validate_custom_role)
def assume(arn):
    """Assume a IAM role."""
    with console.status(f"Assume [b][cyan]{arn}[/cyan][/b] role ...", spinner="dots") as status:
        try:
            role = iam.custom.get(arn)
            session.switch_profile(role.profile.name)
            console.log(f"Switched to profile [b]{role.profile.name}[/b]")
            if re.match(MFA_ARN_PATTERN, role.arn):
                # prompt for MFA token
                status.stop()
                mfa_token = click.prompt("Please enter MFA token")
                status.start()
                credentials = session.get_session_token(role.arn, mfa_token)
            else:
                credentials = session.assume_role(arn=role.arn)
            profile = session.set_credentials(credentials)
        except Exception as e:
            console.log(f"Failed to get role: {e}", style="red")
        else:
            cache.set("profile", session.profile.serialize())
            console.log(f"Assumed role [b]{arn}[/b] successfully")
            session.store_aws_config_file(profile, AWS_DEFAULT_SESSION_PROFILE)
            console.log(f"Profile [b]{AWS_DEFAULT_SESSION_PROFILE}[/b] stored in ~/.aws/credentials", style="green")


@cli.command("list")
def list_():
    """List all available IAM roles configured in the setttings file."""
    with console.status("Listing custom roles ...", spinner="dots"):
        roles = iam.custom.list()
        role_table = RoleTable(items=roles.items, columns=["arn", "profile.name", "profile.region"])
        console.print_table(role_table)


@cli.command()
@click.argument("arn", default="", required=False, callback=validate_custom_role)
def get(arn: str):
    """Get a IAM role."""
    with console.status(f"Get role [b][cyan]{arn}[/cyan][/b]...", spinner="dots"):
        role = iam.custom.get(arn, lazy=False)
        console.print(role.extract())
