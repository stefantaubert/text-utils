from typing import List, Optional

from nltk import download
from nltk.tokenize import sent_tokenize
from unidecode import unidecode as convert_to_ascii

from text_utils.adjustments import (collapse_whitespace, expand_abbreviations,
                                    expand_units_of_measure, normalize_numbers,
                                    replace_at_symbols,
                                    replace_big_letter_abbreviations,
                                    replace_mail_addresses)
from text_utils.language import Language
from text_utils.pronunciation import parse_ipa_to_symbols
from text_utils.symbol_format import SymbolFormat
from text_utils.types import Symbols
from text_utils.utils import split_text, symbols_split

IPA_SENTENCE_SEPARATORS = [r"\?", r"\!", r"\."]


def split_ipa_text(text: str) -> List[str]:
  return split_text(text, IPA_SENTENCE_SEPARATORS)


def normalize_en_grapheme_text(text: str) -> str:
  text = convert_to_ascii(text)
  # text = text.lower()
  # TODO datetime conversion
  text = text.strip()
  text = collapse_whitespace(text)
  text = normalize_numbers(text)
  text = expand_abbreviations(text)
  text = expand_units_of_measure(text)
  text = replace_big_letter_abbreviations(text)
  text = replace_mail_addresses(text)
  text = replace_at_symbols(text)
  return text


def normalize_ger_grapheme_text(text: str) -> str:
  text = text.strip()
  text = collapse_whitespace(text)
  return text


def normalize_ipa(text: str) -> str:
  text = text.strip()
  text = collapse_whitespace(text)
  return text


def normalize_chn_grapheme_text(text: str) -> str:
  text = text.strip()
  text = collapse_whitespace(text)
  return text


def text_normalize(text: str, text_format: SymbolFormat, lang: Optional[Language]) -> str:
  if text_format.is_IPA:
    return normalize_ipa(text)
  if text_format == SymbolFormat.PHONEMES_ARPA:
    raise ValueError("Not supported!")

  assert text_format == SymbolFormat.GRAPHEMES

  if lang is None:
    raise ValueError("Language required!")

  if lang == Language.ENG:
    return normalize_en_grapheme_text(text)

  if lang == Language.GER:
    return normalize_ger_grapheme_text(text)

  if lang == Language.CHN:
    return normalize_chn_grapheme_text(text)

  assert False


def text_to_symbols(text: str, text_format: SymbolFormat, lang: Optional[Language]) -> Symbols:
  if text_format.is_IPA:
    return parse_ipa_to_symbols(text)
  if text_format == SymbolFormat.PHONEMES_ARPA:
    raise ValueError("Not supported!")

  assert text_format == SymbolFormat.GRAPHEMES

  if lang is None:
    raise ValueError("Language required!")

  if lang in {Language.ENG, Language.GER, Language.CHN}:
    return tuple(text)

  assert False


def text_to_sentences(text: str, text_format: SymbolFormat, lang: Optional[Language]) -> List[str]:
  if text_format.is_IPA:
    return split_ipa_text(text)
  if text_format == SymbolFormat.PHONEMES_ARPA:
    raise ValueError("Not supported!")

  assert text_format == SymbolFormat.GRAPHEMES

  if lang is None:
    raise ValueError("Language required!")

  if lang == Language.CHN:
    return split_chn_graphemes_text(text)

  if lang == Language.ENG:
    return split_en_graphemes_text(text)

  if lang == Language.GER:
    return split_ger_graphemes_text(text)

  assert False


def symbols_to_words(symbols: Symbols) -> List[Symbols]:
  return symbols_split(symbols, " ")


CHN_SENTENCE_SEPARATORS = [r"？", r"！", r"。"]


def split_chn_graphemes_text(text: str) -> Symbols:
  return split_text(text, CHN_SENTENCE_SEPARATORS)


def split_en_graphemes_text(text: str) -> List[str]:
  download('punkt', quiet=True)
  res = sent_tokenize(text, language="english")
  return res


def split_ger_graphemes_text(text: str) -> List[str]:
  download('punkt', quiet=True)
  res = sent_tokenize(text, language="german")
  return res
