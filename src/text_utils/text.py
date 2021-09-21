from typing import List, Optional, Set

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
from text_utils.types import Symbol, Symbols
from text_utils.utils import (remove_empty_symbols, split_text,
                              symbols_separate, symbols_split, symbols_strip)

IPA_SENTENCE_SEPARATORS = {"?", "!", "."}
CHN_SENTENCE_SEPARATORS = {"？", "！", "。"}


def split_ipa_text(text: str) -> List[str]:
  # TODO seperate not split!
  raise Exception()
  return split_text(text, IPA_SENTENCE_SEPARATORS)


def ipa_symbols_to_sentences(symbols: Symbols) -> List[Symbols]:
  return symbols_to_sentences_core(symbols, separators=IPA_SENTENCE_SEPARATORS)


def symbols_to_sentences_core(symbols: Symbols, separators: Set[Symbol]) -> List[Symbols]:
  sentences = symbols_separate(symbols, separate_symbols=separators)
  sentences = [symbols_strip(sentence, strip={" "}) for sentence in sentences]
  sentences = [remove_empty_symbols(sentence) for sentence in sentences]
  sentences = [sentence for sentence in sentences if len(sentence) > 0]
  return sentences


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


def symbols_to_sentences(symbols: Symbols, symbols_format: SymbolFormat, lang: Optional[Language]) -> List[Symbols]:
  if symbols_format.is_IPA:
    return ipa_symbols_to_sentences(symbols)
  if symbols_format == SymbolFormat.PHONEMES_ARPA:
    raise ValueError("Not supported!")

  assert symbols_format == SymbolFormat.GRAPHEMES

  if lang is None:
    raise ValueError("Language required!")

  if lang == Language.CHN:
    return split_chn_graphemes_symbols(symbols)

  if lang == Language.ENG:
    return split_en_graphemes_symbols(symbols)

  if lang == Language.GER:
    return split_ger_graphemes_symbols(symbols)

  assert False


def symbols_to_words(symbols: Symbols) -> List[Symbols]:
  return symbols_split(symbols, {" "})


def split_chn_graphemes_text(text: str) -> Symbols:
  # TODO seperate not split!
  raise Exception()
  return split_text(text, CHN_SENTENCE_SEPARATORS)


def split_chn_graphemes_symbols(symbols: Symbols) -> List[Symbols]:
  return symbols_to_sentences_core(symbols, separators=CHN_SENTENCE_SEPARATORS)


def split_en_graphemes_symbols(symbols: Symbols) -> List[Symbols]:
  res = split_en_graphemes_text(''.join(symbols))
  sentence_symbols = [text_to_symbols(
    sentence, text_format=SymbolFormat.GRAPHEMES, lang=Language.ENG) for sentence in res]
  return sentence_symbols


def split_en_graphemes_text(text: str) -> List[str]:
  download('punkt', quiet=True)
  res = sent_tokenize(text, language="english")
  return res


def split_ger_graphemes_symbols(symbols: Symbols) -> List[Symbols]:
  res = split_ger_graphemes_text(''.join(symbols))
  sentence_symbols = [text_to_symbols(
    sentence, text_format=SymbolFormat.GRAPHEMES, lang=Language.GER) for sentence in res]
  return sentence_symbols


def split_ger_graphemes_text(text: str) -> List[str]:
  download('punkt', quiet=True)
  res = sent_tokenize(text, language="german")
  return res
