# MEP01: Mnemocards Enhancement Proposals

In version 0.1 there are several pitfalls.  The most important one is how the
library is structured.  The initial design simply works, but it makes it very
difficult to extend the existing code.  It is not easy to:

* Use a YAML file instead of a `*.cards` file.
* Create a completely new file format similar to `*.cards`.
* Specify a different order in the TSV columns of the vocabulary files.
* Reuse audio generation code from another class that is not the
`VocabularyBuilder`.
* Use a different CSS style in the generated cards.
* Create a new card generator with a completely different behaviour.

Those are just some examples of things the community may be interested in.
This *first Mnemocards Enhancement Proposals (MEP01)* describes a new design
that will help Mnemocards to be more flexible and easily extended by other
users.  This is a high-level document, different MEPs with low-level details
will be created later.

When the code reorganisation proposed in this MEP (and related future MEPs) is
fully implemented, Mnemocards will finally be able to move to the long-awaited
*version 1.0*.


## Components

We should start by identifying each of the components that make it possible for
Mnemocards to generate Anki APKG files.  Currently we have something like this:

```mermaid
graph TD
    FILE[Source Files] --> GEN[Builder]
    GEN --> APKG[Anki APKG File]
```

On the one hand we have the files with the content of the cards.  What we call
*builders* are classes that read those files and generate the cards which are
then grouped into APKG files.  In 0.1.5 we have 4 builder classes:
`VocabularyBuilder`, `ExpressionBuilder`, `MarkdownBuilder` and
`AutogenerateBuilder`.  Builders do a lot of things.  Too many things.
Breaking down the builders into smaller units will make things much easier.
The proposed approach has these components easily differentiated:

```mermaid
graph TD
    FILE[Source Files] --> READ[Readers]
    READ --> GEN[Generator]
    STYLE[Style] --> GEN
    UTIL[Utility code] --> GEN
    GEN --> APKG[Anki APKG File]
```

Again, everything starts from the *source files*, with the content of the
cards.  On the other hand, we have a piece of code that reads these files.
This piece of code will support different formats, we call *reader* to the
function in charge of reading data from an specific file format.  We also have
the card creation logic inside of what we call *generators*. Generators define
what the aforementioned source files should contain.  Note that the generator
does not know anything about the file format, it just receive the content of
the cards in the form of Python data structures (dictionaries).  This allows a
lot of flexibility in the source files format.

Every card comes with a style (the way in which cards are displayed to the
user: colour, font type, screen layout...) and should be defined in separated
files, not in the builder or inside of the mnemocards package.  Of course, some
default styles can be provided, but the user should have the possibility of
reading files from any other location.

Part of the card generation code will only be useful for one type of card, but
another part of the code can be reused for several different types of cards.
For example, generating audio from text is common and very useful for language
cards.  This is why we indicate that generators have access to a certain
library of utilities provided by Mnemocards that will facilitate the repetition
of common and repetitive tasks.

Mnemocards should also have some code that orchestrates this full process.
Mnemocards will call the function that reads the files, pass the information
from the different cards to the generator, pack all the cards into an APKG
file... Mnemocards is just the director that makes these components to work in
harmony.


## Version 1.0

Splitting the current code into the small independent modules outlined in the
previous point will be a milestone for Mnemocards: version 1.0. This MEP01
represents the will to improve the framework with a more flexible and easily
maintainable code, other MEPs will be created to deal with each of the
following points separately:

* [MEP02](mep02.md): New configuration files. Backwards compatibility and migration plan.
* [MEP03](mep03.md): Source files and readers.
* [MEP04](mep04.md): Generators and Mnemocards utilities.
