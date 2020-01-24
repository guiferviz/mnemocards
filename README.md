
<img src="doc/_static/images/logo.png" width="200">

Generate Anki cards from text files (TSV and Markdown).

Text files are easily maintainable, `apkg` files are not.
You can easily store text files in a version control system like *git*, so you
can easily keep track of changes and collaborate with others.

You can generate different kind of cards:
 * **Language cards**:
 Specially designed to learn a language.
 There are two types of language cards:
   * **Vocabulary cards**:
   Cards displayed in 2 languages, your native language and the language you
   are learning.
   * **Expression cards**:
   When you already know a language and want to master it, sometimes it is no
   longer enough to translate into your language, but you want to write
   sentences in the language you are learning with their respective explanation
   also in the language you are learning.
 * **Markdown cards**:
 Cards generated from `*.cards` files.
 This file format has been created in a specific for the creation of cards.
 Apart from a pair of start and end of card markers, the syntax of these files
 is Markdown.
 You can use images, Latex and math in the content of this cards.


## Language cards

<img src="doc/_static/images/vocabulary_card.png" width="200">
<img src="doc/_static/images/expression_card.png" width="200">


## Markdown cards

<img src="doc/_static/images/markdown_img_card.png" width="200">
<img src="doc/_static/images/markdown_code_card.png" width="255">
<img src="doc/_static/images/markdown_math_card.png" width="255">


# Requirements

 * Python 3 and all the libraries listed in `requirements.txt`.
 All these requirements are automatically installed when you install the
 package with `python setup.py install`.
 If you want to install the requirements manually just use:
 `pip install -r requirements.txt`.
 * If you want to import automatically the generated packages, you should have
 Anki installed.
 * If you want to generate cards from your repositories or gists you should
 have Git installed.
 Install it with in Ubuntu-like systems with `apt-get install git`.
 Also, in order to use the GitHub API you should have a file with and API key
 with gists/repository permissions.
 The repository permission is only needed for private repositories.


# Install

Clone this repository, move to the root of the project and run:
```bash
python setup.py install
```


# VIM syntax file for '*.cards'

I'm a die-hard VIM user, for that reason I've created a `cards.vim` syntax
file.
It's not too fancy (I would like to add syntax color to the header of the
cards in the future) but it looks better than using the Markdown syntax.

<img src="doc/_static/images/vim_markdown_syntax.png" width="800">
<img src="doc/_static/images/vim_cards_syntax.png" width="800">

I also use the plugin [Markdown Preview][1] so I can see how my cards look like
without generating the package.
It's not perfect for the `*.cards` format, but it's better than nothing :)


[1]: https://github.com/iamcco/markdown-preview.nvim

