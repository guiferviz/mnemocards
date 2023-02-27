from mnemocards import Task


class NumberGenerator(Task):
    """Yield a series of numbers."""

    def __init__(self, numbers_to_generate=3):
        self.numbers_to_generate = numbers_to_generate

    def process(self, notes):
        for i in range(self.numbers_to_generate):
            yield {"number": i}
        yield from notes


class NumberDouble(Task):
    """Create a `double` property with the value of `number` multiply by 2."""

    def process_one(self, note):
        note["double"] = note["number"] * 2
        return note


class NumberPrint(Task):
    """Print number notes in a custom way."""

    def process_one(self, note):
        number = note["number"]
        double = note["double"]
        print(f"Number {number}, double {double}")
