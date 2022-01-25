from enum import IntEnum
from typing import Generator

from text_utils.types import Symbols
from text_utils.utils import (symbols_ignore, symbols_join, symbols_split,
                              symbols_split_iterable)

String = str
TextString = String
SymbolsString = String

SPACED_WORD_SEP = "  "
SPACED_SYMBOL_SEP = " "

TEXT_WORD_SEP = " "
TEXT_SYMBOL_SEP = ""

TUPLE_WORD_SEP = " "


class StringFormat(IntEnum):
  TEXT = 0
  SYMBOLS = 1

  def convert_string_to_symbols(self, string: String) -> Symbols:
    return convert_string_to_symbols(string, self)

  def convert_symbols_to_string(self, symbols: Symbols) -> String:
    return convert_symbols_to_string(symbols, self)

  def can_convert_string_to_symbols(self, string: String) -> bool:
    return can_convert_string_to_symbols(string, self)

  def can_convert_symbols_to_string(self, symbols: Symbols) -> bool:
    return can_convert_symbols_to_string(symbols, self)


def can_convert_string_to_symbols(string: String, string_format: StringFormat) -> bool:
  if string_format == StringFormat.SYMBOLS:
    return can_convert_symbols_string_to_symbols(string)
  if string_format == StringFormat.TEXT:
    return True
  assert False


def can_convert_symbols_to_string(symbols: Symbols, string_format: StringFormat) -> bool:
  if string_format == StringFormat.SYMBOLS:
    return can_convert_symbols_to_symbols_string(symbols)
  if string_format == StringFormat.TEXT:
    return True
  assert False


def get_other_format(string_format: StringFormat) -> StringFormat:
  if string_format == StringFormat.SYMBOLS:
    return StringFormat.TEXT
  if string_format == StringFormat.TEXT:
    return StringFormat.SYMBOLS
  assert False


def convert_string_to_symbols(string: String, string_format: StringFormat) -> Symbols:
  if string_format == StringFormat.SYMBOLS:
    return convert_symbols_string_to_symbols(string)
  if string_format == StringFormat.TEXT:
    return convert_text_string_to_symbols(string)
  assert False


def convert_symbols_to_string(symbols: Symbols, string_format: StringFormat) -> String:
  if string_format == StringFormat.SYMBOLS:
    return convert_symbols_to_symbols_string(symbols)
  if string_format == StringFormat.TEXT:
    return convert_symbols_to_text_string(symbols)
  assert False


def can_convert_symbols_string_to_symbols(symbols_string: String) -> bool:
  words = symbols_string.split(SPACED_WORD_SEP)
  for word in words:
    if word.startswith(SPACED_SYMBOL_SEP) or word.endswith(SPACED_SYMBOL_SEP):
      return False
  return True


def convert_symbols_string_to_symbols(symbols_string: SymbolsString) -> Symbols:
  assert can_convert_symbols_string_to_symbols(symbols_string)
  words = symbols_string.split(SPACED_WORD_SEP)
  words_symbols = [tuple(word.split(SPACED_SYMBOL_SEP)) for word in words]
  result = symbols_join(words_symbols, join_symbol=TUPLE_WORD_SEP)
  result = symbols_ignore(result, ignore={""})
  return result


def can_convert_symbols_to_symbols_string(symbols: Symbols) -> bool:
  if "" in symbols:
    return False
  words = symbols_split(symbols, split_symbols=TUPLE_WORD_SEP)
  symbols = (symbol for word in words for symbol in word)
  for symbol in symbols:
    symbol_is_no_space_but_contains_space = symbol != SPACED_SYMBOL_SEP and SPACED_SYMBOL_SEP in symbol
    if symbol_is_no_space_but_contains_space:
      return False
  return True


def convert_symbols_to_symbols_string(symbols: Symbols) -> SymbolsString:
  assert can_convert_symbols_to_symbols_string(symbols)
  words = symbols_split(symbols, split_symbols=TUPLE_WORD_SEP)
  words_symbols_str = (SPACED_SYMBOL_SEP.join(word_symbols) for word_symbols in words)
  symbols_str = SPACED_WORD_SEP.join(words_symbols_str)
  return symbols_str


def convert_text_string_to_symbols(text_string: TextString) -> Symbols:
  result = tuple(text_string)
  return result


def convert_symbols_to_text_string(symbols: Symbols) -> TextString:
  result = TEXT_SYMBOL_SEP.join(symbols)
  return result


def get_words(symbols: Symbols) -> Generator[Symbols, None, None]:
  words = symbols_split_iterable(symbols, TUPLE_WORD_SEP)
  words_without_empty = (word for word in words if len(word) > 0)
  return words_without_empty
