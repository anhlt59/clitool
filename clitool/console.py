from rich.console import Console as RichConsole

from clitool.types import CliTable


class LiveType:
    UPDATE = 0
    INSERT = 1


class Console(RichConsole):
    # @staticmethod
    # def generate_table(items: list[list], columns: list[str] = None) -> Table:
    #     """Make a new table."""
    #     table = Table(box=box.SIMPLE, expand=True)
    #     default_column_style = {"justify": "left", "style": "white", "overflow": "fold"}
    #
    #     for column in columns:
    #         column = {**default_column_style, **column}
    #         table.add_column(**column)
    #
    #     for item in items:
    #         table.add_row(*item)
    #     return table
    def print_table(self, cli_table: CliTable):
        self.print(cli_table.table)

    # def live_table(
    #     self, table: CliTable, items: Iterator, live_type: str = LiveType.UPDATE, refresh_per_second: int = 1
    # ):
    #     """Show live table."""
    #     with Live(table.table, refresh_per_second=refresh_per_second) as live:
    #         for item in items:
    #             if live_type == LiveType.INSERT:
    #                 table.add_row(item)
    #             elif live_type == LiveType.UPDATE:
    #                 if isinstance(item, CliItem):
    #                     live.update(table.update_table([item]))
    #                 else:
    #                     live.update(table.update_table(item))
    #             else:
    #                 raise ValueError(f"Invalid live_type: {live_type}")


console = Console()
