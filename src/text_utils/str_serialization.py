from typing import Generator, Iterable

from text_utils.types import Symbol


def can_serialize(symbols: Iterable[str], split_symbol: Symbol) -> bool:
  for symbol in symbols:
    if split_symbol in symbol and symbol != split_symbol:
      return False
  return True


def str_serialization(symbols: Iterable[str], split_symbol: Symbol) -> str:
  assert len(split_symbol) == 1
  text = split_symbol.join(symbols)
  return text


def can_deserialize(text: str, split_symbol: Symbol) -> bool:
  no_of_subsequent_split_symbols = 1
  for char in text:
    if char == split_symbol:
      no_of_subsequent_split_symbols += 1
    else:
      if no_of_subsequent_split_symbols % 2 == 0:
        return False
      no_of_subsequent_split_symbols = 0
  if no_of_subsequent_split_symbols % 2 == 0:
    return True
  return False


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
