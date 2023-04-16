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
* Include extra content in the markdown file that will not be included in a
card.
* Visualize your cards outside Anki using Mkdocs.
* Search your cards database using the build-in Mkdocs search tool.
* Cards database easy to publish thanks to Mkdocs.
