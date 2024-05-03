import os
import re
from difflib import unified_diff
from itertools import islice
from subprocess import PIPE, Popen
from typing import Any, Iterable

from rich.text import Text

mfa_compiler = re.compile(r"(^arn:aws:iam::\d+:mfa/[\w\-_]+$)|(^\d{6,}$)")


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


def execute_command(command: str, stdin=PIPE, stdout=PIPE):
    """
    Run a command and return the output.
    :param command: command to run
    :param stdin: standard input
    :param stdout: standard output
    :return: output of the command
    """
    args = command.split()
    with Popen(args, stdin=stdin, stdout=stdout, stderr=PIPE) as proc:
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            raise Exception(f"COMMAND ERRROR: {stderr.decode('utf-8')}")
        return stdout


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
