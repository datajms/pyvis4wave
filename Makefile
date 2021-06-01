.PHONY: docs build

flake:
	flake8 vis4wave setup.py

install:
	pip install -e ".[test]"

develop:
	pip install -e ".[dev]"
	pre-commit install
	python setup.py develop

test:
	pytest --nbval-lax --disable-warnings --cov=vis4wave tests

clean:
	rm -rf .pytest_cache
	rm -rf build
	rm -rf dist
	rm -rf pyvis4wave.egg-info
	rm -rf .ipynb_checkpoints
	rm -rf .coverage*
	rm -rf tests/.ipynb_checkpoints

black:
	black --check .

test-notebooks:
	pytest --nbval-lax docs/guide/notebooks/*.ipynb

check: black flake clean

pypi: clean
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*
