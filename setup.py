
import os
from os import listdir

from setuptools import setup, find_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements


PACKAGE_NAME = "mnemocards"
DESCRIPTION = "My module description"
KEYWORDS = "python library code"
AUTHOR = "guiferviz"
AUTHOR_EMAIL = "guiferviz@gmail.com"
LICENSE = "Copyright " + AUTHOR
URL = "https://github.com/guiferviz/mnemocards"


# Creates a __version__ variable.
with open(os.path.join(PACKAGE_NAME, "_version.py")) as file:
    exec(file.read())

# Read requirements.
req = parse_requirements("requirements.txt", session="hack")
REQUIREMENTS = []#[str(ir.req) for ir in req]
DEPENDENCY_LINKS = []
for i in req:
    if i.req is not None:
        REQUIREMENTS.append(str(i.req))
    else:
        DEPENDENCY_LINKS.append(str(i.link))
print("Requirements:", REQUIREMENTS)
print("Dependency links:", DEPENDENCY_LINKS)

# Install all packages in the current dir except tests.
PACKAGES = find_packages(exclude=["tests", "tests.*"])
print("Packages:", PACKAGES) 

DATA_FOLDER = "assets"
DATA_FILES = []
for root, dirs, files in os.walk(DATA_FOLDER):
    if len(files) > 0:
        DATA_FILES.append((root, [os.path.join(root, f) for f in files]))
print("Data:", DATA_FILES)

setup(name=PACKAGE_NAME,
      version=__version__,
      description=DESCRIPTION,
      long_description=open("README.md").read(),
      long_description_content_type="text/markdown",
      url=URL,
      keywords=KEYWORDS,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      packages=PACKAGES,
      install_requires=REQUIREMENTS,
      dependency_links=DEPENDENCY_LINKS,
      entry_points={
          "console_scripts": [
              "{} = {}.__main__:main".format(PACKAGE_NAME, PACKAGE_NAME)
          ]
      },
      include_package_data=True,
      data_files=DATA_FILES,
      zip_safe=False)

