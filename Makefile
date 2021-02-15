all:
	@echo "Specify a target."

docs:
	pdoc3 --html --force --output-dir ./docs/api ./supermark
	supermark --all --input ./pages --output ./docs

pypi: docs
	sudo python2 setup.py register sdist upload

code:
	python3 -m isort .
	python3 -m black .

dev-install: docs
	rm -rf ./dist
	python3 setup.py sdist
	python3 -m pip install -v -U dist/*.tar.gz

deploy: docs
	rm -rf ./dist
	python3 setup.py sdist
	twine upload dist/*

pep8:
	pep8-python2 pdoc/__init__.py scripts/pdoc

push:
	git push origin master
	git push github master

test:
	python3 -m pytest -s tests/test_sites.py

coverage:
	coverage run -m pytest tests/test_sites.py
	coverage html -d coverage_html