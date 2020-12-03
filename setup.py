from setuptools import find_packages, setup

setup(
    dependency_links=[
        "git+https://github.com/stefantaubert/cmudict-parser.git@e8767cfdd2e1405890afc5a3566f33b4c6e75a2d#egg=cmudict-parser"
    ],
    name="text_utils",
    version="1.0.0",
    url="https://github.com/stefantaubert/text-utils.git",
    author="Stefan Taubert",
    author_email="stefan.taubert@posteo.de",
    description="Utils for text processing",
    packages=["text_utils"],
    install_requires=[
        "click==7.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "dragonmapper==0.2.6",
        "editdistance==0.5.3",
        "epitran==1.8",
        "hanzidentifier==1.0.2",
        "inflect==5.0.2",
        "ipapy==0.0.9.0",
        "joblib==0.17.0; python_version >= '3.6'",
        "marisa-trie==0.7.5",
        "munkres==1.1.4",
        "nltk==3.5",
        "numpy==1.19.4; python_version >= '3.6'",
        "panphon==0.17",
        "pyyaml==5.3.1",
        "regex==2020.11.13",
        "tqdm==4.54.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "unicodecsv==0.14.1",
        "unidecode==1.1.1",
        "wget==3.2",
        "zhon==1.1.5",
    ],
)
