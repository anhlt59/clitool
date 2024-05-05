import logging

import click
from rich.logging import RichHandler

from clitool.constants import LOG_FORMAT

logger = logging.getLogger()
for h in logger.handlers:
    logger.removeHandler(h)

handler = RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])
handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(handler)

__all__ = ["logger"]
