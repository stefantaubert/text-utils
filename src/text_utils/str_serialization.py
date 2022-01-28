from typing import Generator, Iterable

from text_utils.types import Symbol


def can_serialize(symbols: Iterable[str], split_symbol: Symbol) -> bool:
  pass


def str_serialization(symbols: Iterable[str], split_symbol: Symbol) -> str:
  assert len(split_symbol) == 1
  text = split_symbol.join(symbols)
  return text


def can_deserialize(text: str, split_symbol: Symbol) -> bool:
  last_char_was_split_symbol = True
  for char in text:
    pass


def str_deserialization(text: str, split_symbol: Symbol) -> Generator[Symbol, None, None]:
  #assert can_deserialize(text, split_symbol)
  assert len(split_symbol) == 1
  symbol = ""
  yield_subsequent_split_symbol = None
  for char in text:
    if char == split_symbol:
      if symbol == "":
        if yield_subsequent_split_symbol is None:
          yield char
          yield_subsequent_split_symbol = False
        elif yield_subsequent_split_symbol:
          yield char
          yield_subsequent_split_symbol = False
        else:
          yield_subsequent_split_symbol = True
      else:
        yield symbol
        symbol = ""
        yield_subsequent_split_symbol = True
    else:
      symbol += char
  if symbol != "":
    yield symbol
