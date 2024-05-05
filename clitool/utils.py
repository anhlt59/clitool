import os
import subprocess
import sys
from difflib import unified_diff
from itertools import islice
from typing import Any, Iterable, Literal

from rich.text import Text

PROC_OUTPUT = Literal["PIPE", "STDOUT", "DEVNULL"]


def execute_command(command: str, output: PROC_OUTPUT = "PIPE") -> str:
    """
    Run a command and return the output.
    :param command: (str) command to run
    :param output: STDOUT  - sys stdout
                   PIPE    - return output
                   DEVNULL - discard output
    :return: output of the command
    """
    match output:
        case "STDOUT":
            stdout = sys.stdout
        case "PIPE":
            stdout = subprocess.PIPE
        case "DEVNULL":
            stdout = subprocess.DEVNULL
        case _:
            raise ValueError("Invalid output type, use 'PIPE', 'STDOUT' or 'DEVNULL'")

    with subprocess.Popen(
        command.split(),
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdout=stdout,
        universal_newlines=True,
        bufsize=-1,
    ) as process:
        if stdout == subprocess.DEVNULL:
            return ""
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise Exception(f"COMMAND ERRROR: {stderr}")
        return stdout


def chunks(objs: Iterable[Any], limit: int) -> Iterable[list[Any]]:
    """
    Yield successive limit-sized chunks from a iterable.
    :param objs: list of any objects
    :param limit: chunk size
    :return: iterable limit-sized chunks
    """
    if isinstance(objs, list) or isinstance(objs, tuple):
        objs = iter(objs)
    while batch := list(islice(objs, limit)):
        yield batch


def list_files(directory: str) -> Iterable[str]:
    """
    List all files in a directory.
    :param directory: directory path
    :return: list of files
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)


def rich_diff(text1: str, text2: str) -> Text | None:
    """
    Compare two texts and return the difference.
    :param text1: text 1
    :param text2: text 2
    :return: difference if any or None
    """
    result = Text()
    diff = list(unified_diff(text1.splitlines(), text2.splitlines()))

    if len(diff) == 0:
        return None

    for line in diff:
        line = line.strip("\n")
        if line.startswith("-"):
            result.append(f"{line}\n", style="red")
        elif line.startswith("+"):
            result.append(f"{line}\n", style="green")
        else:
            result.append(f"{line}\n", style="white")
    return result
