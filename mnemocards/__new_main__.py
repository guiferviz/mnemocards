import sys

import typer
from loguru import logger

from mnemocards._version import __version__
from mnemocards.commands import cook

APP_NAME = "mnemocards"
APP_WELCOME_LOGO = """
███    ███ ███    ██ ███████ ███    ███  ██████   ██████  █████  ██████  ██████  ███████
████  ████ ████   ██ ██      ████  ████ ██    ██ ██      ██   ██ ██   ██ ██   ██ ██
██ ████ ██ ██ ██  ██ █████   ██ ████ ██ ██    ██ ██      ███████ ██████  ██   ██ ███████
██  ██  ██ ██  ██ ██ ██      ██  ██  ██ ██    ██ ██      ██   ██ ██   ██ ██   ██      ██
██      ██ ██   ████ ███████ ██      ██  ██████   ██████ ██   ██ ██   ██ ██████  ███████
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"""

app = typer.Typer()


def say_hello():
    typer.secho(APP_WELCOME_LOGO, fg=typer.colors.BRIGHT_BLUE)
    typer.secho(f"Version: {__version__}", fg=typer.colors.BRIGHT_MAGENTA)


@app.callback()
def callback(verbose: bool = typer.Option(False, "--verbose", "-v")):
    logger.remove()
    say_hello()
    if verbose:
        logger.add(sys.stderr, level="TRACE")
    else:
        logger.add(sys.stderr, level="CRITICAL")


app.command("cook")(cook.main)


if __name__ == "__main__":
    app()
