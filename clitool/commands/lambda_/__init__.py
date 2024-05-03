from click_shell import shell

from .function import cli as function_cli
from .layer import cli as layer_cli


@shell("lambda", prompt="AWS ❯ Lambda ❯ ")
def cli():
    """AWS Lambda."""
    pass


cli.add_command(function_cli)
cli.add_command(layer_cli)

__all__ = ["cli"]
