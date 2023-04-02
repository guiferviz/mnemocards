# Plugins

This example will demonstrate how to create custom Mnemocards tasks to process
your flashcards in any way you desire.

!!! warning

    This example assumes a basic knowledge of Python. If you are not familiar
    with Python, it is recommended that you first learn the basics of the
    language before attempting to create custom Mnemocards tasks.

We will be generating a sequence of numbers using a for loop, multiplying each
number by a factor of 2, and then printing the resulting numbers. All that
using custom Mnemocards tasks.

!!! example

    You can find the final source code for this example [in the repo]({{
    config.repo_url }}/tree/main/examples/plugins).


## Setup

The custom tasks will be defined in a `plugins.py` Python module, located in
the same directory as your `mnemocards.yaml` configuration file.

!!! warning

    The name `plugins.py` is arbitrary, and you can choose any name you prefer.
    However, some names may hide existing Python modules, so using names like
    `os`, `sys`, or `mnemocards` for your plugin file would be problematic.

As the first step, create an empty directory for this example. Inside that
directory, create two empty files: `mnemocards.yaml` and `plugins.py`.


## Data source

Every Mnemocards pipeline usually begins with a task that reads data from a
source. Without data in our pipeline, there would be nothing to process.
Therefore, the first thing we are going to do in our example is to create a
task that injects cards into the main pipeline.

It is common to read information from a file or a web resource, but to simplify
the example, we will simply generate a series of consecutive numbers.

```python title="plugins.py"
from mnemocards import Task


class NumberGenerator(Task):
    """Yield a series of numbers."""
    def process(self, _):
        for i in range(3):
            yield {"number": i}
```

To create a custom task, you will first define a class that extends the
`mnemocards.Task` base class. In this class, you can implement the process
method to perform any transformations on the input data or generate new input
data. You can also implement the `start` and `end` methods to perform any setup
and teardown tasks that your task requires.

Once you have defined your custom task class, you can use it in your
`mnemocards.yaml` configuration file by specifying the fully qualified class
name as the task type. Update your config file with the following content:

```yaml title="mnemocards.yaml"
steps:
  - type: plugin.NumberGenerator
  - type: Print
```

In this configuration file we are telling Mnemocards that we want to run our
number generator first and then, just to make sure it is working correctly, we
print each of the generated dictionaries.

If you run `mnemocards run` from a terminal in the project directory, you will
see an output similar to:

```cmd
$ mnemocards run
╔╦╗╔╗╔╔═╗╔╦╗╔═╗┌─┐┌─┐┬─┐┌┬┐┌─┐
║║║║║║║╣ ║║║║ ║│  ├─┤├┬┘ ││└─┐
╩ ╩╝╚╝╚═╝╩ ╩╚═╝└─┘┴ ┴┴└──┴┘└─┘ 1.0.0a0
╭───────────────────────────────────────────────────────────────────────────────────╮
│ I have a photographic memory... I need to take a photograph to remember anything. │
╰───────────────────────────────────────────────────────────────────────────────────╯
Hi! 👋
Looking for config files... 📃
✨  Valid task found in `mnemocards.yaml` ✨
╭─ Note 0 ──╮
│ number: 0 │
╰───────────╯
╭─ Note 1 ──╮
│ number: 1 │
╰───────────╯
╭─ Note 2 ──╮
│ number: 2 │
╰───────────╯
See you soon! 🤙.
```


## Configuration parameters

In the previous section, we generated a fixed number of cards using a hardcoded
value inside the Python `range` function. However, we may want to change this
value from our configuration file.

To achieve this, we can modify the `NumberGenerator` class to accept a parameter
`numbers_to_generate` which defaults to 3. We can then use this parameter to
control the number of cards to generate.

```python title="plugins.py"
from mnemocards import Task


class NumberGenerator(Task):
    """Yield a series of numbers."""
    def __init__(self, numbers_to_generate=3):
        self.numbers_to_generate = numbers_to_generate

    def process(self, _):
        for i in range(self.numbers_to_generate):
            yield {"number": i}
```

If we do not modify our previous config file, `numbers_to_generate` will take
the default value of 3, so the output will be the same.

Now, we can use this parameter in our YAML configuration file. In the following
example, we set `numbers_to_generate` to 2:

```yaml title="mnemocards.yaml"
steps:
  - type: plugin.NumberGenerator
    numbers_to_generate: 2
  - type: Print
```

The output of this pipeline shows that only two cards were generated:

```cmd
╭─ Note 0 ──╮
│ number: 0 │
╰───────────╯
╭─ Note 1 ──╮
│ number: 1 │
╰───────────╯
```

By changing the value of `numbers_to_generate` in our YAML configuration file,
we can easily control the number of cards generated by our pipeline. Any other
parameter present in our YAML file will be passed to the `__init__` method.


## Upstream cards

Our implementation has a problem. Try to run this configuration file:

```yaml title="mnemocards.yaml"
steps:
  - type: plugin.NumberGenerator
    numbers_to_generate: 1
  - type: plugin.NumberGenerator
    numbers_to_generate: 1
  - type: Print
```

We may think that we should get two cards, one from each generator:

```cmd
╭─ Note 0 ──╮
│ number: 0 │
╰───────────╯
╭─ Note 1 ──╮
│ number: 0 │
╰───────────╯
```

However, what we actually get is:

```cmd
╭─ Note 0 ──╮
│ number: 0 │
╰───────────╯
```

This card is generated by our second `NumberGenerator`, but the card from the
first one is not reaching the `Print` task. Why? This is because the `process`
method that we are using to inject data also receives an iterable of elements
that come from the previous task. At the moment, we are completely ignoring the
first argument of `process`, so if we want our generator not to ignore the
previous cards, we need to modify our class as follows:

```python title="plugins.py"
from mnemocards import Task


class NumberGenerator(Task):
    """Yield a series of numbers."""
    def __init__(self, numbers_to_generate=3):
        self.numbers_to_generate = numbers_to_generate

    def process(self, notes):
        yield from notes
        for i in range(self.numbers_to_generate):
            yield {"number": i}
```

Now we are giving a name to the notes parameter and we are making our generator
return all the notes/dictionaries generated by the previous tasks first, and
then inject its own. This way, the output will be as expected:

```cmd
$ mnemocards run
╔╦╗╔╗╔╔═╗╔╦╗╔═╗┌─┐┌─┐┬─┐┌┬┐┌─┐
║║║║║║║╣ ║║║║ ║│  ├─┤├┬┘ ││└─┐
╩ ╩╝╚╝╚═╝╩ ╩╚═╝└─┘┴ ┴┴└──┴┘└─┘ 1.0.0
╭──────────────────────────────────────────────────────────────────────────────────────────╮
│ My memory is so bad, I could plan my own surprise birthday party and still be surprised. │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
Hi! 👋
Looking for config files... 📃
✨  Valid task found in `mnemocards.yaml` ✨
╭─ Note 0 ──╮
│ number: 0 │
╰───────────╯
╭─ Note 1 ──╮
│ number: 0 │
╰───────────╯
See you soon! 🤙
```


## Process notes

Our previous task generates data. Let's create a task that just process the
existing data. In the same `plugins.py` file add the following class:

```python title="plugins.py"
class NumberDouble(Task):
    """Create a `double` property with the value of `number` multiply by 2."""
    def process(self, notes):
        for note in notes:
            note["double"] = note["number"] * 2
            yield note
```

In the `mnemocards.yaml` file, include the following steps:

```yaml title="mnemocards.yaml"
steps:
  - type: plugin.NumberGenerator
    numbers_to_generate: 3
  - type: plugin.NumberDouble
  - type: Print
```

The printed cards should be:

```cmd
╭─ Note 0 ──╮
│ number: 0 │
│ double: 0 │
╰───────────╯
╭─ Note 1 ──╮
│ number: 1 │
│ double: 2 │
╰───────────╯
╭─ Note 2 ──╮
│ number: 2 │
│ double: 4 │
╰───────────╯
```

To simplify the code, you can overwrite the `process_one` method instead of
process. This method receives one note at a time instead of an iterable with
all the upstream notes:

```python title="plugins.py"
class NumberDouble(Task):
    """Create a `double` property with the value of `number` multiply by 2."""
    def process_one(self, note):
        note["double"] = note["number"] * 2
        return note
```

The result should be exactly the same.


## Sink tasks

In addition to generating and processing cards, it is also necessary to produce
something with them. For instance, creating Anki decks. The Print function we
have been using throughout this tutorial is also a way to perform an action
with the pipeline data.

The following is an example of a custom print task, which inherits from the
Task class and defines a `process_one` method that takes a note as input. The
note is a dictionary containing the number and double fields.

```python title="plugins.py"
class NumberPrint(Task):
    """Print number notes in a custom way."""
    def process_one(self, note):
        number = note["number"]
        double = note["double"]
        print(f"Number {number}, double {double}")
        return note
```

!!! note

    The `return note` is needed to keep the flow of notes. If no return is used
    the notes are not going to *survive* after the `NumberPrint` task. In other
    words, our task will act as a filter.

The task is then added to the pipeline along with the previously defined
`NumberGenerator` and `NumberDouble` tasks:

```yaml title="mnemocards.yaml"
steps:
  - type: plugin.NumberGenerator
    numbers_to_generate: 3
  - type: plugin.NumberDouble
  - type: plugin.NumberPrint
```

Finally, running the pipeline produces the following output:

```cmd
Number 0, double 0
Number 1, double 2
Number 2, double 4
```


## Complete code

See the [complete code in the repo]({{ config.repo_url
}}/tree/main/examples/plugins).


## Conclusion

Using custom tasks in Mnemocards allows you to tailor the card processing
pipeline to your specific needs. For example, you can create tasks to
automatically generate pronunciations, add images or audio files, or perform
complex text processing operations. The possibilities are endless, and with
Mnemocards, you have the power to customize your flashcard creation process in
any way you see fit.

--8<-- "examples/plugins/README.md"
