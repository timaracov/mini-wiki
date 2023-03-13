__version__ = "0.0.1"


import setuptools


setuptools.setup(
    name="pywiki",
    version=__version__,
    description="easy wiki builder from mardown files",
    author="timaracov",
    author_email="neyenburgz@mail.ru",
    packages=setuptools.find_packages(),
    python_requires=">=python3.10",
)
