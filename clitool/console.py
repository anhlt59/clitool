from rich.console import Console as RichConsole

from clitool.types import CliTable


class LiveType:
    UPDATE = 0
    INSERT = 1


class Console(RichConsole):
    def print_table(self, cli_table: CliTable):
        self.print(cli_table.table)


console = Console()
