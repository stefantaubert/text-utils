# text-utils

methods:

```py
def text_normalize(text: str, lang: Language, logger: Logger) -> str:
  ...
def text_to_ipa(text: str, lang: Language, mode: Optional[EngToIpaMode], replace_unknown_with: Optional[str], logger: Logger) -> str:
  ...
def text_to_sentences(text: str, lang: Language, logger: Logger) -> List[str]:
  ...
def text_to_symbols(text: str, lang: Language, ipa_settings: Optional[IPAExtractionSettings], logger: Logger) -> List[str]:
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

### Add to another project

In the destination project run:

```sh
# if not already done:
pip install --user pipenv --python 3.7
# add reference
pipenv install -e git+https://github.com/stefantaubert/text-utils.git@master#egg=text_utils
```

## Dev

update setup.py with shell and `pipenv-setup sync`
see [details](https://pypi.org/project/pipenv-setup/)

## Examples

There are files containing an example map and example symbols in the folder examples. You can use them to test the client. The commands are the following:

### For printing the map

If you want to print the pretrained weights mapping, use

```sh
pipenv run python -m text_utils.cli print_map \
  --path="examples/examplemap.json" \
  --arrow_type="weights"
```

If you want to print the map showing all occuring symbols and the corresponding synthesizable symbols that are assigned to them, use

```sh
pipenv run python -m text_utils.cli print_map \
  --path="examples/examplemap.json" \
  --arrow_type="inference"
```

### For printing the symbols

If you want to print all allowed symbols, use

```sh
pipenv run python -m text_utils.cli print_symbols \
  --path="examples/examplesymbols.symb"
```

### For changing

If you want to change the symbol for a specific key, use

```sh
pipenv run python -m text_utils.cli change_symbols \
  --path="examples/examplemap.json" \
  --symbol_path="examples/examplesymbols.symb" \
  --arrow_type="weights"
```

or

```sh
pipenv run python -m text_utils.cli change_symbols \
 --path="examples/examplemap.json" \
 --symbol_path="examples/examplesymbols.symb" \
 --arrow_type="inference"
```

(depending on the use case)
and follow the instructions.

It is also possible to change one symbol without the interactive mode via for example

```sh
pipenv run python -m text_utils.cli change_symbols \
  --path="examples/examplemap.json" \
  --symbol_path="examples/examplesymbols.symb" \
  --to_key="ʒ" \
  --map_symbol="ʌ"
```

where `"ʒ"` is the key to which `"ʌ"` is newly assigned.
