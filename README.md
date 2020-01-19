
<img src="logo.png" width="200">

Here you have the Python scripts I use for generating my Anki cards.
With this scripts you can easily generate cards from TSV and Markdown files.


# Requirements

* Python 3 and all the libraries listed in `requirements.txt`.
Install them with `pip install -r requirements.txt`.
* If you want to generate cards from your gists you should have Git installed.
Install it with `apt-get install git`.
Also, in order to use the GitHub API you should have a `~/.gist` file with and API key with Gists permissions.
* Python libraries listed in `requirements.txt`.


# TODO

* archivo de configuración global con los repos a clonar
    * opción de clonar todos los gist
* escanear recursivamente todos los directorios y buscar un cards.config que contenga los packages que queremos crear, de qué ficheros salen, que templates se utilizan...
* generar assets y paquetes en el directorio donde se encuentre el cards.config o donde lo indique la configuración global.

