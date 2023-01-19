import mnemocards


class CLI:
    def __init__(self, version: bool = False):
        if version:
            self._greet()
            raise SystemExit()

    def _greet(self):
        print(mnemocards.__version__)

    def hi(self, name: str = "guiferviz"):
        """Say hello.

        Args:
            name (str): Your name.
        """
        print(f"Hi {name}")

    def bye(self, name: str = "guiferviz"):
        """Say good bye.

        Args:
            name (str): Your name.
        """
        print(f"Bye {name}")
