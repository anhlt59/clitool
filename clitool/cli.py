import click
import click_completion
from click_shell import Shell, shell
from rich import pretty, traceback

from clitool import commands
from clitool.cache import cache
from clitool.commands.base import tree
from clitool.services import SessionService
from clitool.types.session import Profile


def install_context(ctx: click.Context):
    session = SessionService()

    if profile_data := cache.get("profile"):
        profile = Profile.deserialize(profile_data)
        session.switch_profile(profile.name)
        # if credentials has been expired, refresh it
        if profile.credentials.is_expired():
            from clitool.commands.session import refresh

            ctx.invoke(refresh)
        else:
            session.set_credentials(profile.credentials)

    ctx.ensure_object(dict)
    ctx.obj["session"] = session
    return ctx


@shell("aws", prompt="AWS ❯ ")
@click.option("--debug/--no-debug", default=False, required=False, help="Enable debug mode.")
@click.pass_context
def cli(ctx, debug):
    if debug:
        traceback.install()
    pretty.install()
    install_context(ctx)

    @ctx.call_on_close
    def close():
        cache.set("profile", ctx.obj["session"].profile.serialize())
        cache.save()


def main():
    def add_default_command(command):
        if isinstance(command, Shell):
            command.add_command(tree)
            for sub_command in command.commands.values():
                add_default_command(sub_command)
        return command

    # build the command collection
    click_completion.init()
    cli.add_command(commands.session)
    cli.add_command(commands.iam)
    cli.add_command(commands.dynamodb)
    cli.add_command(commands.s3)
    cli.add_command(commands.lambda_)
    cli.add_command(commands.cloudformation)
    cli.add_command(commands.secretsmanager)
    add_default_command(cli)
    cli()


if __name__ == "__main__":
    main()
