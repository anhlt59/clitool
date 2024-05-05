import time

import click
from click_shell import shell

from clitool.commands.base import validate_file, validate_required_value
from clitool.console import console
from clitool.services import LambdaService, SessionService
from clitool.types.lambda_ import LambdaLayerTable, PublishLayerConfig, Runtimes

from .base import validate_runtime

session = SessionService()
lambda_ = LambdaService(session)


# CLI commands ---------------------------------------------------------------
@shell("layer", prompt="AWS ❯ Lambda ❯ Layer ❯ ")
def cli():
    pass


@cli.command("list")
@click.option("-f", "--filter", "name_filter", help="Layer name to filter by", type=str)
@click.option("-r", "--runtime", help="Runtime to filter by", type=str, callback=validate_runtime)
def list_(name_filter: str, runtime: Runtimes | None):
    """List all Lambda layers in the account."""
    with console.status("Listing Lambda layers ...", spinner="dots"):
        try:
            layers = lambda_.layer.list(runtime=runtime, name_filter=name_filter)
        except Exception as e:
            console.log(f"Failed to list Lambda layers: {e}", style="red")
        else:
            table = LambdaLayerTable(
                items=layers.items, columns=["name", "description", "runtimes", "version", "created_date"]
            )
            console.print_table(table)


@cli.command()
@click.argument("name", default="", required=False, callback=validate_required_value)
def get(name: str):
    """Get a Lambda layer by name."""
    with console.status(f"Getting [b]{name}[/b] layer ...", spinner="dots"):
        try:
            layer = lambda_.layer.get(name)
        except Exception as e:
            console.log(f"Failed to get Lambda layer: {e}", style="red")
        else:
            console.print(layer.extract())


@cli.command()
@click.pass_context
def publish(ctx):
    from clitool.commands.s3 import upload_file

    # Publish headless browser layer
    ctx.invoke(
        upload_file,
        bucket="",
        key="deployment_packages/lambda_layers/headless-browser-layer.zip",
        path="layers/headless-browser-layer.zip",
    )
    with console.status("Publishing [green][b]chromium-layer[/b][/green] layer ...", spinner="dots"):
        try:
            layer = lambda_.layer.publish(
                PublishLayerConfig(
                    name="chromium-layer",
                    description=f"{round(time.time())}",
                    runtimes=["python3.10", "python3.11", "python3.12"],
                    archive=PublishLayerConfig.PublishLayerArchive(
                        s3_bucket="",
                        s3_key="deployment_packages/lambda_layers/headless-browser-layer.zip",
                    ),
                )
            )
            console.log("[b]di2-chromium[/b] layer has been published successfully", style="green")
        except Exception as e:
            console.log(f"Failed: {e}", style="red")
        else:
            console.print(layer.extract())


@cli.command()
@click.option("--runtime", help="Lambda runtime", default="python3.12", type=str, callback=validate_runtime)
@click.option("--requirement", help="Requirements file", default="", type=str, callback=validate_file)
def export(runtime, requirement):
    """Export a Lambda layer."""
    try:
        lambda_.layer.export_python_layer(runtime, requirement)
    except Exception as e:
        console.log(f"Failed to export Lambda layer: {e}", style="red")
    else:
        console.print("Done! 🚀", style="green")
