# MEP02: Configuration files

A `cards_config.json` is the configuration file in Mnemocards 0.1.  In order to
implement the improvements proposed in MEP01 the configuration files must be
slightly changed.  This MEP02 describes the necessary changes and describes the
plan to follow to avoid backwards compatibility problems.


## Why `cards_config` is a JSON? Can I use YAML?

Mnemocards version 1.0 features full format flexibility, so why force
configuration files to be in only one format?

Although JSON is a widely used format and sometimes the favourite of many
people, other formats such as YAML are much more human-friendly.  For example,
look at the last 8 lines of `examples/english/cards_config.json`:

```
                            }
                        }
                    ]
                }
            ]
        }
    ]
}
```

Lovely, aren't they? Omitting any of those characters would cause a read error.
YAML doesn't have that kind of problem, it results in more compact and easier
to write files.  It is also not necessary to use `"` quotes in YAML files.

Forcing the use of YAML in configuration files would go against the ideas of
v1.0, so why not keep everyone happy and support both formats?

The new configuration files will be `mnemocards.json` or `mnemocards.yaml`.
Why not `cards_config.json` and `cards_config.yaml`?  The main reasons are as
follows:

* The new name _advertises_ Mnemocards :) For anyone who finds a directory with
a file called mnemocards and doesn't know the library, a single Google search
would be enough to find it and learn how to use it. On the other hand, a Google
search for "cards_config" will give you results that are not related to the
Mnemocards Python library.
* To facilitate the development of v1.0 while preserving backwards
compatibility. More information about this in the next section.


## Backwards compatibility

Version 0.1 has been alive for a long time and some people have already created
their card collection using Mnemocards. We should not break existing card
repositories and we cannot force anyone to update all their
`cards_config.json`.

The solution to this problem is simple if you rename the configuration file.
If `cards_config.json` is in the source folder then use code from Mnemocards
v0.1. If `mnemocards.json` or `mnemocards.yaml`, then use code from Mnemocards
v1.0.  This way you can add new features to the library without affecting
existing features at all.  The key part here is to ADD, i.e. never modify
existing builder's code.


## Migration plan

At the moment there is no plan to create a migration script from
`cards_config.json` to `mnemocards.json`, but it is feasible and would not be
hard to do.


## New configuration structure

Most of the configuration file will remain intact, only the src property will
be changed.  In order to split the builders in more maintainable pieces as
suggested in MEP01, we need to clearly separate the configuration options of
the reader from the configuration options of the generator.

This is an example of object inside the `src` property in v0.1:

```json title="cards_config.json, inside the src property in v0.1."
{
    "type": "vocabulary",
    "file": "hiragana.tsv",
    "header": true,
    "pronunciation_in_reverse": false,
    "card_color": "#33AA33",
    "furigana": false,
    "audio": {
        "lang": "ja",
        "media_dir": "media/hiragana"
    },
    "card_properties": {
        "tags": ["japanese", "hiragana"]
    }
}
```

All the entries of this dictionary where passed to the builder.  The proposed
structure is:

```json title="mnemocards.json, inside the src property in v1.0."
{
    "path": "hiragana.tsv",
    "generator": "vocabulary",
    "media_output_dir": "media/hiragana",
    "default_card_properties": {
        "card_color": "#33AA33",
        "tags": ["japanese", "hiragana"],
        "audio_lang": "ja",
        "furigana": false,
        "pronunciation_in_reverse": false
    }
}
```

The `path` property will contain all the information needed by the reader. How
readers work will be explained in more detail in MEP03.  Same happens with the
`generator` property, it will be described in detail in MEP04.  For now we can
consider that `path` contains the name of the file in a supported format and
`generator` contains the name of the generator that will be used to transform
the dictionaries read by the reader into Anki cards.

`media_output_dir` is a property common to all generators.  Mnemocards should
facilitate the generation of audio and the inclusion of images on the cards.
As this is common to all generators, this option is separate from the
generator.

You can assign any default property to the dictionaries returned by the reader.
Those default values are in `default_card_properties`.  All the cards inside
`hiragana.tsv` will have `"furigana": false` if the furigana column does not
exists in the TSV file.  If the furigana column exists in the TSV and some
values different from NULL or empty string are provided, the default value
won't be used.  Properties like tags, i.e. properties with a list as value,
will be appended to the existing value.  This means that if we have a tags
column in the TSV file with a value `vowel`, the final tags property for that
card will be `["japanese", "hiragana", "vowel"]`.
