# MEP03: Readers

In the current implementation (v0.1) builders are responsible of reading the
input files.  This leads to two main problems:

1. The code for reading input files is duplicated on every builder. Even if you
move the code to a function and you reuse that function, the builder is still
in charge of calling that function.
2. The file format depends on the generator, there is no easy way of accepting
different formats.

In the VocabularyBuilder code, not only it is specified that TSV has to be the
input format, but it also forces you to use the same column order as the
specified in this nasty line:

```python title="vocabulary_builder.py"
note_id, ylw, yle, lylw, lylp, lyle, row_tags = row
```

In this MEP we define how the reading of files should be done in v1.0.


## Module `any2dict`

We propose to create a function within Mnemocards with the following signature:
`any2dict(path, **options)`. It takes as input a path to a directory or file
and options specific to each of the formats. For example, for a CSV file a
possible option would be the delimiter.

Imagine we have the following file in the `data` directory:

```csv title="data/cards.csv"
front,back
front1,back1
front2,back2
```

The expected output of `any2dict("data/cards.csv", delimiter=",")` is a Python
dictionary with the following structure:

```json title="Output (Python dictionary)"
{
    "data/cards.csv": [
        {"front": "front1", "back": "back1"},
        {"front": "front2", "back": "back2"},
    ]
}
```

Imagine now that there is a YAML file in the same directory.

```yaml title="data/cards.yaml"
- front: front1
  back: back1
- front: front2
  back: back2
```

The expected output of `any2dict("data/", delimiter=",")` is:

```json title="Output (Python dictionary)"
{
    "data/cards.csv": [
        {"front": "front1", "back": "back1"},
        {"front": "front2", "back": "back2"},
    ],
    "data/cards.yaml": [
        {"front": "front1", "back": "back1"},
        {"front": "front2", "back": "back2"},
    ]
}
```

When you read more than one file at the same time, readers will only get those
options that they understand. In this example, the option `delimiter=","` is
just passed to the CSV reader.

There are formats like TOML that return a dictionary, not a list of
dictionaries as expected.

```toml title="data/cards.toml"
[[cards]]
front = front1
back = back1

[[cards]]
front = front1
back = back1
```

The output of calling `any2dict("data/cards.toml")` is:

```python title="TOML Output"
{
    "data/cards.toml": {
        "cards": [
            {
                "front": "front1",
                "back": "back1",
            },
            {
                "front": "front2",
                "back": "back2",
            }
        ]
    },
}
```

The only requirement for Mnemocards is that, at some point of the output we
should have a list of dictionaries.  In this example, the cards property inside
data/cards.toml contains a list, so Mnemocards will assume that the card
dictionaries are inside that list.


## Reader class

Readers should implement the following methods:

```python title="reader.py"
class Reader:
    extensions = []

    def load(self, path, **options):
        pass

    def loads(self, string, **options):
        pass
```

`extensions` is a list of strings with the file extensions that this reader can
read.  `load` reads from a file and `loads` reads from a string, similar to
`json.load` and `json.loads` from the standard Python JSON module.

Following the comparison to the JSON module, this would be a possible
implementation of a JSON reader.

```python title="json_reader.py"
class JSON(Reader):
    extensions = ["json"]

    def load(self, path, **options):
        return json.load(path, **options)

    def loads(self, string, **options):
        return json.loads(string, **options)
```


## Extensions

Mnemocards must provide a way to register readers, so that anyone can define a
new format.  Mnemocards extensions or plugins will create reader classes that
will be registered in the library so that the `any2dict` function can use them.

The proposed way of registering readers in Mnemocards is using a decorator in
your reader class. For example:

```python title="extension.py"
import mnemocards

@mnemocards.add_reader
class MyReader...
```

This way we can extend Mnemocards even from an external library, without even
modifying the Mnemocards source code.


## Reading configuration files

We can use the `any2dict` function to read configurations files.  This allows
users to write their configurations files in the format that they prefer.  They
can even create a new reader just for reading configuration files.


## Options in configuration files

In MEP02 we defined the new configuration files. In the hiragana example we
have:

```json
{
    "path": "hiragana.tsv"
}
```

If no more options need to be passed to the reader, this is a common way of set
the reader.  Imagine now that you have a SSV file (Semicolon Separated
Values), how can you read that file using the CSV reader with a different
delimiter?  This is the way of providing extra information to the readers in
the configuration file:

```json
{
    "path": {
        "path": "hiragana.ssv",
        "reader": "csv",
        "delimiter": ","
    }
}
```
