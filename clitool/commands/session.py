import click
from click_shell import shell

from clitool.commands.base import validate_required_value
from clitool.console import console
from clitool.services import SessionService
from clitool.settings import AWS_DEFAULT_SESSION_PROFILE
from clitool.types.session import ProfileTable
from clitool.utils import mfa_compiler

session = SessionService()


# Validators ------------------------------------------------------------------
def validate_profile(ctx=None, param=None, name="") -> str:
    name = name.strip(" \n")
    profiles = session.list_profiles()
    profile_names = [profile.name for profile in profiles.items]

    # if profile_name is not None, check if it exists in the list of profiles
    # else try to get the profile from cache
    if name == "":
        if cached_profile := ctx.obj.get("profile"):
            return validate_profile(ctx, param, cached_profile.arn)
    elif name in profile_names:
        return name
    else:
        console.clear()
        console.log(f"Profile(name='{name}') not found", style="yellow")

    # if cache is empty or profile is not found, prompt the user to choose a profile
    profile_table = ProfileTable(items=profiles.items, columns=["name", "region"])
    console.print_table(profile_table)
    return validate_profile(ctx, param, click.prompt("Please choice a profile name"))


# CLI commands ---------------------------------------------------------------
@shell("session", prompt="AWS ❯ Session ❯ ")
def cli():
    """Session management."""
    pass


@cli.command(help="List all available profiles on your system.")
def list_profiles():
    """List all available profiles on your system."""
    with console.status("Listing profiles ...", spinner="dots"):
        profiles = session.list_profiles()
        profile_table = ProfileTable(items=profiles.items, columns=["name", "region"])
        console.print_table(profile_table)


@cli.command(help="Get current profile.")
def current_profile():
    """Get a profile."""
    with console.status("Get current profile ...", spinner="dots"):
        session.profile = session.get_profile(session.profile.name, region_name=session.profile.region, lazy=False)
        console.print(session.profile.extract())


@cli.command(help="Get a profile by name.")
@click.argument("name", required=False, default="", callback=validate_profile)
def get_profile(name):
    """Get a profile.
    :param name: Profile name
    """
    with console.status(f"Get [b][cyan]{name}[/cyan][/b] profile...", spinner="dots"):
        try:
            profile = session.get_profile(name, lazy=False)
        except Exception as e:
            console.log(f"Profile {name} is inactive: {e}", style="red")
        else:
            console.print(profile.extract())


@cli.command(help="Switch to a profile.")
@click.argument("name", default="", required=False, callback=validate_profile)
def switch_profile(name: str):
    """Switch to a profile.
    :param name: Profile name
    """
    if session.profile.name == name:
        console.log(f"Already in {name} profile", style="yellow")
    else:
        with console.status(f"Switching to [b][cyan]{name}[/cyan][/b] profile ...", spinner="dots"):
            try:
                profile = session.switch_profile(name)
            except Exception as e:
                console.log(f"Failed to switch {name} profile: {e}", style="red")
                raise click.Abort()

        console.log(f"Switched to {profile}")
        session.store_aws_config_file(profile, AWS_DEFAULT_SESSION_PROFILE)
        console.log(f"Profile [b]{AWS_DEFAULT_SESSION_PROFILE}[/b] stored in ~/.aws/credentials", style="green")


@cli.command(help="Refresh the session token.")
def refresh_token():
    """Refresh the session token."""
    credentials = session.profile.credentials
    if credentials.aws_expiration is None:
        console.log("Permanent credentials, no need to refresh", style="yellow")
    else:
        with console.status("Refreshing session token ...", spinner="dots") as status:
            try:
                if mfa_compiler.match(credentials.aws_arn):
                    status.stop()
                    mfa_token = click.prompt("Please enter MFA token")
                    status.start()
                    credentials = session.get_session_token(credentials.aws_arn, mfa_token)
                else:
                    credentials = session.assume_role(credentials.aws_arn)
            except Exception as e:
                console.log(f"Failed to refresh session token: {e}", style="red")
                raise click.Abort()

            session.set_credentials(credentials)
            session.store_aws_config_file(session.profile, AWS_DEFAULT_SESSION_PROFILE)
            console.log(f"Profile [b]{AWS_DEFAULT_SESSION_PROFILE}[/b] has been refreshed", style="green")


@cli.command(help="Change region.")
@click.argument("region", default="", required=False, callback=validate_required_value)
def change_region(region: str):
    """Change region."""
    # if the current region is the same with passed region, do nothing
    if session.profile.region == region:
        console.log(f"Already in {region} region", style="yellow")
    else:
        with console.status("Changing region ...", spinner="dots"):
            try:
                profile = session.change_region(region)
            except Exception as e:
                console.log(f"Failed to change region: {e}", style="red")
            else:
                console.print(profile.extract())
                console.log(f"Region changed to {region}", style="green")
