from mnemocards import Task


class NumberGenerator(Task):
    def __init__(self, numbers_to_generate):
        self.numbers_to_generate = numbers_to_generate

    def process(self, notes):
        # Yield a series of numbers.
        for i in range(self.numbers_to_generate):
            yield i
        # The following yield is a good practice when defining generator
        # classes. It yields all the notes that are already in the pipeline.
        yield from notes


class Print(Task):
    def process_one(self, note):
        # Do something with your notes:
        print(f"Print note: {note}")
