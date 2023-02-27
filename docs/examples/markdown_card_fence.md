# [WIP] Markdown Card Fence

!!! failure "Work In Progress"

    This page will contain an example on how to embed cards in markdown files.
    Using a markdown plugin we can also generate HTML code from our cards.


=== "Generated HTML"

    This is some **markdown** file. You can embed cards inside markdown using
    the following syntax:

    <<<
    id: 12345
    tags: tag0, tag1
    ===
    Title
    ---
    Back
    >>>

=== "Markdown source code"

    ```markdown
    This is some **markdown** file. You can embed cards inside markdown using
    the following syntax:

    <<<
    id: 12345
    tags: tag0, tag1
    ===
    Title
    ---
    Back
    >>>
    ```


## Features

* Build several cards inside the same Markdown file.
* Visualize your cards outside Anki.
* Search your cards database using Mkdocs search tool.
* Cards database easy to publish thanks to Mkdocs.
