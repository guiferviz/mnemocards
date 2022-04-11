# MEP04: Generators

In this MEP we define the structure of a generator. A generator has the task of
creating cards from a data structure with all the necessary information about
it. The creation of a card involves the creation of an object that will later
be handled by the genanki packager and the preparation of any multimedia file
associated with the card (images or sound generation).

The terminology "card" and "note" are inherited from Anki. A note is basically
a high-level structure containing data and information on how to create cards.
Cards are what we finally see and study. For example, imagine you are learning
Spanish, your note for "hello" would be represented by the top square in the
following diagram. From that note two cards would be generated, one with
English on the front and one with Spanish on the front. It is very common even
in the documentation to find that we talk about cards when we should say notes.
Although this nomenclature can be confusing, we hope that from the context it
is clear what exactly is being referred to.

// Edit this diagram in https://asciiflow.com/
```
    ┌───────────────────────────┐
    │  your_language: Hello     │
    │  language_you_learn: Hola │
    └───┬────────────────────┬──┘
        │                    │
        ▼                    ▼
 ┌───────────┐          ┌───────────┐
 │   Hola    │          │   Hello   │
 │ --------- │          │ --------- │
 │   Hello   │          │   Hola    │
 └───────────┘          └───────────┘
```

You can read a better explanation about cards, notes and field in the
https://docs.ankiweb.net/getting-started.html#notes--fields[Anki documentation].

A generator needs two things to work: a correct definition of what input data
is expected and the instructions for converting that input data into a note.


## Input data validation

One design option would be to define generators as a class with a generate
method that accepts a dictionary. That dictionary should contain everything
necessary to generate notes from it, i.e. our class would be assuming that the
dictionary passed to it would have all the required data and in the correct
data type.

```python title="generator.py"
class Generator:
    def generate(card_data: dict) -> Note:
        pass
```

The problem with this approach is that we cannot be sure what kind of data are
we expecting without reading the full generate function. If any of the fields
are not mandatory, to find out what the default value is, we have to read the
whole function again to see where that value is used. Renaming fields is not so
easy in dictionaries, refactor tools does not include renaming strings
with dictionary keys and search and replace is error prone.

For these reasons it is proposed to use a data structure similar to a Python
dataclass that allows us to validate the input data before calling the generate
function. This frees the generator from data validation and specifying default
values. The https://pydantic-docs.helpmanual.io[pydantic] library is a good
candidate for this, using the type annotation and validators is possible to
clearly separate the definition of the expected data from the code that
generates it. This new data structure is what we call a CardModel.


## Link a CardModel to a Generator

So far we have clearly differentiated 2 parts of the generation process: the
data model (validation and default values) and the generator. A generator will
only work if it receives the correct data model. Somewhere in the mnemocards
code we need to take a dictionary from the reader, create the data model and
pass it to the generator. How do we know which model should we create for a
given generator?

A possible option is to specify the type as a property of the object:

```python title="generator.py"
class CardModel(BaseModel):
    pass


class Generator:
    card_model = CardModel

    def generate(card_model) -> Note:
        pass
```

This way, knowing the generator you can get which CardModel to use. Although
this is a valid option, the suggested way is more elegant. It is proposed that
the type annotations of the data_model parameter tell mnemocards which
DataModel to use. In this way, in addition to saving a line, the developer is
forced to make use of the type annotations, with all the advantages that this
implies.

```python title="generator.py"
class CardModel(BaseModel):
    pass


class Generator:
    def generate(card_model: CardModel) -> Note:
        pass
```

With a generator object and a the
https://docs.python.org/3/library/inspect.html#inspect.signature[inspect.signature]
Python method we can get that the class Generator need a card model of the
CardModel class.


## Output of a generator

A generator is a class with one main method: generate. The input of `generate`
is a CardModel. What about the expected output? We need to return not just a
note, but also the multimedia files associated to it.

```python title="generator.py"
class Generator:
    def generate(card_properties):
        return genanki.NoteID, multimedia
```

The multimedia files are expected as a list of paths.

While having to return the media files is an extra task that Mnemocards could
do to make it easier for the generators, for the time being we will opt for
this design because it is quite similar to how the current (v0.1.5) Builder are
implemented.
