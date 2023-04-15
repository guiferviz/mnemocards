<p align="center">
    <a href="https://guiferviz.github.io/mnemocards" target="_blank">
        <img src="https://guiferviz.com/mnemocards/images/logo.jpg"
             alt="Mnemocards logo"
             width="200">
    </a>
</p>
<p align="center">
    <a href="https://github.com/guiferviz/mnemocards/actions/workflows/cicd.yaml" target="_blank">
        <img src="https://github.com/guiferviz/mnemocards/actions/workflows/cicd.yaml/badge.svg"
             alt="Mnemocards CI pipeline status">
    </a>
    <a href="https://app.codecov.io/gh/guiferviz/mnemocards/" target="_blank">
        <img src="https://img.shields.io/codecov/c/github/aidictive/mnemocards"
             alt="Mnemocards coverage status">
    </a>
    <a href="https://github.com/guiferviz/mnemocards/issues" target="_blank">
        <img src="https://img.shields.io/github/issues/guiferviz/mnemocards"
             alt="Mnemocards issues">
    </a>
    <a href="https://github.com/aidictive/mnemocards/graphs/contributors" target="_blank">
        <img src="https://img.shields.io/github/contributors/guiferviz/mnemocards"
             alt="Mnemocards contributors">
    </a>
    <a href="https://pypi.org/project/mnemocards/" target="_blank">
        <img src="https://pepy.tech/badge/mnemocards"
             alt="Mnemocards total downloads">
    </a>
    <a href="https://pypi.org/project/mnemocards/" target="_blank">
        <img src="https://pepy.tech/badge/mnemocards/month"
             alt="Mnemocards downloads per month">
    </a>
    <br />
    In addition to helping you memorise, this code helps you do other things that I don't remember...
</p>

---

:books: **Documentation**:
<a href="https://guiferviz.com/mnemocards" target="_blank">
    https://guiferviz.com/mnemocards
</a>

:keyboard: **Source Code**:
<a href="https://github.com/guiferviz/mnemocards" target="_blank">
    https://github.com/guiferviz/mnemocards
</a>

---

## 🤔 What is this?

**Mnemocards** is a Python package originally intended for creating Anki
flashcards from text files. It allows users to define a series of steps to read
flashcards from any source, transform them and export them to different formats
such as Anki APKG packages.

Mnemocards is designed to be fully extensible, which means that users can
create their own tasks and customize the card generation process to their
specific needs. Indeed, Mnemocards has the versatility to be used for purposes
beyond generating Anki decks.


## 🏷️ Features

* **Generate Anki APKG packages** that you can later import into the Anki app.
* Auto **generate pronunciations** from the words that you are learning in any
language supported by Google Translator.
* Generate **flashcards from text files** that can be stored in Git
repositories. This brings several positive things:
    * Keep **track of changes**.
    * Edit cards using your **favourite text editor**. I :heart: VIM.
    * Easily **share and collaborate with others**. If you know how to work
    with Git you can create forks and pull requests to existing repositories.
* **Fully extensible architecture** that allows you to define custom
transformations on a list of notes.
    * Possibility to implement another way of exporting flashcards to other
      existing flashcards apps. Contributions are welcome.
    * Possibility to create search indexes, analyze your collection of cards,
      create visualizations, clustering, analyze how the cards relate to each
      other... Contributions are welcome.


## ⚙️ Installation

To get started with Mnemocards, you'll need to have Python >= 3.10 installed on
your computer. Then, you can install Mnemocards using `pip`:

```cmd
$ pip install --pre mnemocards
```

You can check that the installation went well by executing the following
command:

```cmd
$ mnemocards --version
╔╦╗╔╗╔╔═╗╔╦╗╔═╗┌─┐┌─┐┬─┐┌┬┐┌─┐
║║║║║║║╣ ║║║║ ║│  ├─┤├┬┘ ││└─┐
╩ ╩╝╚╝╚═╝╩ ╩╚═╝└─┘┴ ┴┴└──┴┘└─┘ X.Y.Z
╭────────────────────────────────╮
│ <A super mega funny joke here> │
╰────────────────────────────────╯
```

If the joke made you laugh you can continue with this tutorial, otherwise this
program is not for you and you should consider other alternatives.


## 🤓 How it works?

Once you have Mnemocards installed, you can start creating your own flashcards.
Let's start creating our own vocabulary Anki cards.

Mnemocards uses a configuration file named `mnemocards.yaml` to define the
steps that will be used to process the flashcards. In this file, you can
specify the tasks that you want to use, the order in which they will be
executed, and any necessary parameters.

Here's an example of a simple configuration file that reads in a CSV file
containing flashcard data, and then generates an Anki APKG package:

```yaml
steps:
  - type: ReadFile
    path: flashcards.csv
  - type: Anki
    deck:
      name: My Flashcards
      id: b45f6d48-d1ab-4d0e-80a9-08a2ab473a41
    note_type:
      type: BasicNoteType
  - type: Package
```

In this example, the first step reads in a CSV file called "flashcards.csv", the second step generates an Anki package with a deck named "My Flashcards" and a specific id, and the last step creates the APKG package.

You can run the configuration file using the mnemocards command:

```cmd
$ mnemocards run mnemocards.yml
```

This will execute the steps in the configuration file, and create the Anki APKG package.

You can also use the package to export your flashcards to other flashcard apps like Quizlet by adding a Quizlet task to the configuration file and providing the necessary credentials.

With Mnemocards, you can customize the flashcard generation process to suit your needs and easily collaborate with others. Give it a try and see how it can help you learn more efficiently!
