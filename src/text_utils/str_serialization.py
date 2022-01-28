from typing import Generator

from text_utils.types import Symbol


def can_serialize(text: str, split_symbol: Symbol) -> bool:
  if split_symbol * 2 in text:
    if not split_symbol * 3 in text:
      pass


def str_deserialization(text: str, split_symbol: Symbol) -> Generator[Symbol, None, None]:
  #assert can_serialize(text, split_symbol)
  symbol = ""
  split_symbol_before = False
  for char in text:
    if char != split_symbol:
      symbol += char
    elif symbol != "":
      yield symbol
      symbol = ""
      split_symbol_before = True
    elif split_symbol_before:
      yield split_symbol
      split_symbol_before = False
    else:
      split_symbol_before = True
  if symbol != "":
    yield symbol
