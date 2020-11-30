# text-utils

methods:

```py
def text_normalize(text: str, lang: Language) -> str:
  ...
def text_to_ipa(text: str, lang: Language, mode: Optional[EngToIpaMode]) -> str:
  ...
def text_to_sentences(text: str, lang: Language) -> List[str]:
  ...
def text_to_symbols(text: str, lang: Language, ignore_tones: Optional[bool] = None, ignore_arcs: Optional[bool] = None) -> List[str]:
  ...
```

## Setup

Currently there is only linux supported.

You need to install [flite](https://github.com/festvox/flite) for G2P conversion of English text with Epitran for OOV words:

```sh
git clone https://github.com/festvox/flite
cd flite
./configure && make
sudo make install
cd testsuite
make lex_lookup
sudo cp lex_lookup /usr/local/bin
cd ..
```

Then checkout this repository:

```sh
git clone https://github.com/stefantaubert/text-utils.git
cd textgrid-ipa
python3.8 -m pip install pipenv
python3.8 -m pipenv install --dev
```
