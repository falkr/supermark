docs:
    supermark build --all --input . --output ./docs
    #    pdoc3 --html --force --output-dir ./docs/api ./supermark

pypi: #docs
    sudo python2 setup.py register sdist upload

code:
    python3 -m isort .
    python3 -m black .

dev-install: #docs
    rm -rf ./dist
    python3 setup.py sdist
    python3 -m pip install -v -U dist/*.tar.gz

deploy: #docs
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

conda:
	conda env remove -n supermark-dev
	conda create --yes python=3.10.0 -n supermark-dev
	conda activate supermark-dev
	python3 -m pip install --upgrade pypandoc  markdown-it-py pyyaml colorama click openpyxl progressbar2 pygments wikitextparser requests cairosvg pathlib2 tqdm indentation blindspin beepy watchdog pretty_errors rich icecream black blindspin pytest coverage