import json

import click

from clitool.console import console
from clitool.types.lambda_ import Runtimes


# Validators ------------------------------------------------------------------
def validate_payload(ctx, param, payload: str) -> dict:
    if not payload:
        payload = click.prompt("Please enter a payload")
    try:
        return json.loads(payload)
    except json.JSONDecodeError as e:
        console.log(f"Invalid JSON payload: {e}", style="yellow")
        return validate_payload(ctx, param, click.prompt("Please enter a payload"))


def validate_runtime(ctx, param, runtime: str) -> str | None:
    if runtime and runtime not in Runtimes.__args__:
        console.log(f"Invalid runtime. Supported runtimes: {Runtimes.__args__}", style="yellow")
        return validate_runtime(ctx, param, click.prompt("Please enter a runtime"))
    return runtime
