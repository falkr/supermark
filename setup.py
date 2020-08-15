import codecs
import os.path
from distutils.core import setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


package_name = "supermark"

setup(
    name=package_name,
    packages=[package_name],
    version=get_version("{}/__init__.py".format(package_name)),
    description="Pandoc-based transformation tool for documents containing different markup languages.",
    # long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    install_requires=[
        "pypandoc",
        "pyyaml",
        "colorama",
        "click",
        "openpyxl",
        "progressbar2",
        "pygments",
        "wikitextparser",
        "requests",
        "cairosvg",
        "pathlib",
    ],
    package_data={"": ["*.tex", "*.pdf"],},
    include_package_data=True,
    author="Frank Alexander Kraemer",
    author_email="kraemer.frank@gmail.com",
    license="GPLv3",
    url="https://github.com/falkr/supermark",
    download_url="https://github.com/falkr/supermark/archive/0.2.tar.gz",
    keywords=["education"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": ["supermark=supermark.command:run"]},
)
