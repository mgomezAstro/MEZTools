import os
from setuptools import setup
from meztools.version import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="meztools",
    version=__version__,
    author="Marco Gómez",
    author_email="mgomez_astro@outlook.com",
    description=(
        "Program to convert wavelenght calirbated FITS into velocity calibrated FITS."
    ),
    packages=["meztools"],
    long_description=read("README.rst"),
)

