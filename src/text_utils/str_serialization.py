from typing import Generator, Iterable

from text_utils.types import Symbol


def can_serialize(symbols: Iterable[str], split_symbol: Symbol) -> bool:
  pass


def str_serialization(symbols: Iterable[str], split_symbol: Symbol) -> str:
  assert len(split_symbol) == 1
  text = split_symbol.join(symbols)
  return text


def can_deserialize(text: str, split_symbol: Symbol) -> bool:
  if split_symbol * 2 in text:
    if not split_symbol * 3 in text:
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
        if yield_subsequent_split_symbol:
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

# def str_deserialization(text: str, split_symbol: Symbol) -> Generator[Symbol, None, None]:
#   #assert can_deserialize(text, split_symbol)
#   assert len(split_symbol) == 1
#   symbol = ""
#   split_symbol_before = False
#   for char in text:
#     if char != split_symbol:
#       symbol += char
#     else:
#       if symbol != "":
#         yield symbol
#         symbol = ""
#         split_symbol_before = True
#       else:
#         if split_symbol_before:
#           yield split_symbol
#           split_symbol_before = False
#         else:
#           split_symbol_before = True
#   if symbol != "":
#     yield symbol

# def str_deserialization(text: str, split_symbol: Symbol) -> Generator[Symbol, None, None]:
#   #assert can_deserialize(text, split_symbol)
#   assert len(split_symbol) == 1
#   symbol = ""
#   split_symbol_before = False
#   for char in text:
#     if char != split_symbol:
#       symbol += char
#     elif symbol != "":
#       yield symbol
#       symbol = ""
#       split_symbol_before = True
#     elif split_symbol_before:
#       yield split_symbol
#       split_symbol_before = False
#     else:
#       split_symbol_before = True
#   if symbol != "":
#     yield symbol
