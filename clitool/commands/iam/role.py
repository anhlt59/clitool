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
def validate_role(ctx, param, arn: str = "") -> str:
    arn = arn.strip(" \n")
    # validate if the given arn exists in the list of roles
    # else try to get the default role from cache
    if arn == "":
        if cached_role := ctx.obj.get("role"):
            return validate_role(ctx, param, cached_role.arn)
        else:
            return validate_role(ctx, param, click.prompt("Please enter a role arn"))
    else:
        return arn


# CLI commands ---------------------------------------------------------------
@shell("role", prompt="AWS ❯ IAM ❯ Role ❯ ")
def cli():
    pass


@cli.command()
@click.argument("arn", default="", required=False, callback=validate_role)
def assume(arn):
    """Assume a IAM role."""
    with console.status(f"Assume [b][cyan]{arn}[/cyan][/b] role ...", spinner="dots") as status:
        try:
            role = iam.role.get(arn)
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
            console.log(f"🔥 Failed to get role: {e}", style="red")
        else:
            cache.set("profile", session.profile.serialize())
            console.log(f"Assumed role [b]{arn}[/b] successfully")
            session.store_aws_config_file(profile, AWS_DEFAULT_SESSION_PROFILE)
            console.log(f"Profile [b]{AWS_DEFAULT_SESSION_PROFILE}[/b] stored in ~/.aws/credentials", style="green")


@cli.command("list")
def list_():
    """List all available IAM roles configured in the setttings file."""
    with console.status("Listing roles ...", spinner="dots"):
        roles = iam.role.list()
        role_table = RoleTable(items=roles.items, columns=["arn", "profile.name", "profile.region"])
        console.print_table(role_table)


@cli.command()
@click.argument("arn", default="", required=False, callback=validate_role)
def get(arn: str):
    """Get a IAM role."""
    with console.status(f"Get role [b][cyan]{arn}[/cyan][/b]...", spinner="dots"):
        role = iam.role.get(arn, lazy=False)
        console.print(role.extract())
