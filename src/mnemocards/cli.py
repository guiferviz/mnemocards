import logging
import random
import uuid

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.theme import Theme

import mnemocards
from mnemocards.runner import create_and_run_task
from mnemocards.types import PathLike

_LOGO = """
╔╦╗╔╗╔╔═╗╔╦╗╔═╗┌─┐┌─┐┬─┐┌┬┐┌─┐
║║║║║║║╣ ║║║║ ║│  ├─┤├┬┘ ││└─┐
╩ ╩╝╚╝╚═╝╩ ╩╚═╝└─┘┴ ┴┴└──┴┘└─┘
""".strip()
# Some of this jokes have been taken from https://upjoke.com/memory-jokes.
# Some others are made up by guiferviz.
_JOKES = [
    "In addition to helping you memorize, this code helps you do other things that I don't remember.",
    "I have a photographic memory... I need to take a photograph to remember anything.",
    "I used to have a photographic memory, but now I can't even remember where I put my camera.",
    "I can't remember the last time I forgot something, but I'm sure it's not the only thing I've forgotten.",
    "My memory is so bad, I could plan my own surprise birthday party and still be surprised.",
    "My exceptional memory allows me to memorize a sequence of more than a million numbers: 1, 2, 3, 4, 5...",
    "I have the memory of an elephant. I remember seeing an elephant a couple of years ago when I went to the zoo.",
    "I can't remember the last time I forgot something, but I also forgot the last time I remembered something.",
]


class CLI:
    def __init__(self, version: bool = False, log_level: str = "CRITICAL"):
        self._init_console()
        self._init_logging(log_level)
        self._greet()
        if version:
            raise SystemExit()

    def _init_console(self):
        self._console = Console(
            theme=Theme(
                {
                    "logo": "bold green",
                    "version": "bold yellow",
                    "info": "green",
                    "warning": "bold yellow",
                    "joke": "bold italic blue",
                    "log.time": "yellow",
                    "logging.level.info": "bold blue",
                }
            )
        )

    def _init_logging(self, log_level: str):
        self._log_level = log_level
        logging.basicConfig(
            level=log_level,
            format="%(message)s",
            datefmt="%H:%M:%S",
            handlers=[
                RichHandler(
                    show_level=True,
                    show_time=True,
                    rich_tracebacks=True,
                    markup=True,
                    console=self._console,
                )
            ],
        )

    def _greet(self):
        logo = f"[logo]{_LOGO}"
        version = f"[version]{mnemocards.__version__}"
        self._console.print(f"{logo} {version}")
        joke = random.choice(_JOKES)
        self._console.print(Panel.fit(f"[joke]{joke}"))

    def run(self, directory: PathLike = ".", filename: str = "mnemocards.yaml"):
        """Run a given Mnemocard task.

        Args:
            directory: Directory to search for a Mnemocards Task definition.
            filename: File name with the Mnemocards Task configuration.
        """
        self._console.print("[info]Hi! :waving_hand:")
        try:
            create_and_run_task(directory, filename)
        except Exception:
            self._console.print_exception(
                show_locals=self._log_level == "DEBUG"
            )
            self._console.print(
                "[warning]Although things didn't go as well as we expected,"
                " hope to see you soon! :call_me_hand:"
            )
        else:
            self._console.print("See you soon! :call_me_hand:")

    def id(self):
        id_ = str(uuid.uuid4())
        self._console.print(id_)
