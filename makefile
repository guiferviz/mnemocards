POETRY=poetry
PYTEST=$(POETRY) run pytest
GIT=git
GIT_TAG=$(shell $(GIT) describe --tags)
PYTHON_MODULE=mnemocards


build: requirements.txt
	$(POETRY) build

requirements.txt: pyproject.toml
	poetry export -f requirements.txt --output requirements.txt --without-hashes

publish: build
ifdef PYPI_URL
	$(POETRY) config repositories.pypi $(PYPI_URL)
	$(POETRY) publish -r pypi -u __token__ -p $(PYPI_TOKEN) || $(POETRY) config repositories.pypi --unset
else
	$(POETRY) publish -u __token__ -p $(PYPI_TOKEN)
endif

install:
	$(POETRY) install
	$(POETRY) run pre-commit install

format_and_lint:
	$(POETRY) run pre-commit run --all

test:
	$(POETRY) run coverage run --source=src/ -m pytest tests/
	$(POETRY) run coverage report
	$(POETRY) run coverage xml
	$(POETRY) run coverage html

doc:
	$(POETRY) run mkdocs build

doc-publish:
	$(POETRY) version $(GIT_TAG)
	$(POETRY) run mkdocs gh-deploy --force

doc-serve:
	mkdocs serve

complete-zsh:
	$(PYTHON_MODULE) -- --completion | sed 's/:/: /g' > completion
	@echo "To activate completion in your zsh shell, run the command" \
		" 'source ./completion'. If you want to keep the completion active " \
		" after closing your terminal session, you can also add the command" \
		" 'source <path to your project>/completion' to your ~/.zshrc file."
