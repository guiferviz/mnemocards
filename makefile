POETRY=poetry
PYTEST=$(POETRY) run pytest
PACKAGE=mnemocards


build: requirements.txt
	$(POETRY) build

requirements.txt: pyproject.toml
	poetry export -f requirements.txt --output requirements.txt --without-hashes

publish: build
	$(POETRY) config repositories.pypi $(PYPI_URL)
	$(POETRY) publish -r pypi -u $(PYPI_USERNAME) -p $(PYPI_PASSWORD)

install:
	$(POETRY) install -E all

test:
	$(PYTEST) --cov=$(PACKAGE) --cov-report=term --cov-report=html tests/
