from enum import IntEnum

from text_utils.str_serialization import (can_deserialize_symbols,
                                          can_serialize_symbols,
                                          deserialize_symbols,
                                          serialize_symbols)
from text_utils.types import Symbols

String2 = str
TextString2 = String2
SymbolsString2 = String2

SPACED_SEP = " "


class StringFormat2(IntEnum):
  DEFAULT = 0
  SPACED = 1

  def convert_string_to_symbols(self, string: String2) -> Symbols:
    return convert_string_to_symbols(string, self)

  def convert_symbols_to_string(self, symbols: Symbols) -> String2:
    return convert_symbols_to_string(symbols, self)

  def can_convert_string_to_symbols(self, string: String2) -> bool:
    return can_convert_string_to_symbols(string, self)

  def can_convert_symbols_to_string(self, symbols: Symbols) -> bool:
    return can_convert_symbols_to_string(symbols, self)


def can_convert_string_to_symbols(string: String2, string_format: StringFormat2) -> bool:
  if string_format == StringFormat2.SPACED:
    return can_deserialize_symbols(string, SPACED_SEP)
  if string_format == StringFormat2.DEFAULT:
    return True
  assert False


def can_convert_symbols_to_string(symbols: Symbols, string_format: StringFormat2) -> bool:
  if string_format == StringFormat2.SPACED:
    return can_serialize_symbols(symbols, SPACED_SEP)
  if string_format == StringFormat2.DEFAULT:
    return True
  assert False


def get_other_format(string_format: StringFormat2) -> StringFormat2:
  if string_format == StringFormat2.SPACED:
    return StringFormat2.DEFAULT
  if string_format == StringFormat2.DEFAULT:
    return StringFormat2.SPACED
  assert False


def convert_string_to_symbols(string: String2, string_format: StringFormat2) -> Symbols:
  assert isinstance(string, str)
  assert isinstance(string_format, StringFormat2)
  if string_format == StringFormat2.SPACED:
    return tuple(deserialize_symbols(string, SPACED_SEP))
  if string_format == StringFormat2.DEFAULT:
    return convert_text_string_to_symbols(string)
  assert False


def convert_symbols_to_string(symbols: Symbols, string_format: StringFormat2) -> String2:
  assert isinstance(symbols, tuple)
  assert isinstance(string_format, StringFormat2)
  if string_format == StringFormat2.SPACED:
    return serialize_symbols(symbols, SPACED_SEP)
  if string_format == StringFormat2.DEFAULT:
    return convert_symbols_to_text_string(symbols)
  assert False


def convert_text_string_to_symbols(text_string: TextString2) -> Symbols:
  result = tuple(text_string)
  return result


def convert_symbols_to_text_string(symbols: Symbols) -> TextString2:
  result = "".join(symbols)
  return result
