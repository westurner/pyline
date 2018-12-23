
# Makefile
APP=pyline

.PHONY: help clean-pyc clean-build docs clean test test-all coverage docs release dist twine docs_rsync_to_local docs_rebuild

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"

clean: clean-build clean-pyc
	rm -fr htmlcov/

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 '$(APP)' tests

test:
	python setup.py test

test-all:
	tox

coverage:
	coverage run --source '$(APP)' setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/$(APP).rst
	rm -f docs/modules.rst
	sphinx-apidoc --no-toc -o docs/ '$(APP)'
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	@#$(MAKE) open docs/_build/html/index.html

_setversion:
	sed -i "s/version='\(.*\)'/version='$(version)'/g" ./setup.py
	sed -i "s/^__version__ =\(.*\)$$/__version__ = '$(version)'/g" pyline/pyline.py

setversion:
	@# Usage:
	@#   make setversion version=0.3.17
	git diff --exit-code ./setup.py ./pyline/pyline.py && \
		echo "ERROR: There are existing changes. Exiting." >&2 && false
	$(MAKE) _setversion version=$(version)
	git diff --exit-code ./setup.py pyline/pyline.py || true
	git commit -m "RLS: setup.py, pyline.py: version=$(version)" \
		setup.py pyline/pyline.py

release:
	@# Usage:
	@#   make release version=0.3.17
	#	 version=v0.3.17
	## Start a new HubFlow release
	git hf release start '$(version)'
	## update version in setup.py and pyline.py
	$(MAKE) setversion version=$(version)
	## register with pypi
	#    python setup.py build register
	## generate a source distribution and upload to pypi
	#python setup.py bdist_wheel upload
	$(MAKE) dist
	git hf release finish '$(version)'
	$(MAKE) twine
	## create a new tagged release
	#    update http://github.com/westurner/pyline/releases
	#	 browse to url, select version tag
	#	 - [ ] click 'Edit release'
	#	 - [ ] set the release title to "pyline v${ver}"
	#	 - [ ] (optionally) paste the changelog into the release description
	python -m webbrowser 'https://github.com/westurner/pyline/releases/edit/$(version)'

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist/*

twine:
	# PyPI: https://pypi.org/account/login/
	twine upload ./dist/*

docs_rsync_to_local:
	rsync -avr ./docs/_build/html/ '$(_DOCSHTML)'/'$(APP)'

docs_rebuild:
	$(MAKE) docs
	$(MAKE) docs_rsync_to_local
