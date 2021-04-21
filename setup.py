from setuptools import find_packages, setup

setup(
    dependency_links=[
        "git+https://github.com/stefantaubert/cmudict-parser.git@1c4cce798af0f76e882f3083ce382ff1317ecc96#egg=cmudict-parser"
    ],
    name="text_utils",
    version="1.0.0",
    url="https://github.com/stefantaubert/text-utils.git",
    author="Stefan Taubert",
    author_email="stefan.taubert@posteo.de",
    description="Utils for text processing",
    packages=["text_utils"],
    install_requires=[
        "epitran",
        "nltk",
        "dragonmapper",
        "ipapy",
        "inflect",
        "unidecode",
    ],
)
