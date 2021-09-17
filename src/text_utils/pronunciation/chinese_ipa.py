import string
from typing import Optional, Set, Tuple

from dragonmapper import hanzi
from sentence2pronunciation.core import sentence2pronunciation_cached
from text_utils.pronunciation.ipa2symb import parse_ipa_to_symbols
from text_utils.pronunciation.ipa_symbols import SCHWAS, TONES, VOWELS
from text_utils.types import Symbol, Symbols
from text_utils.utils import symbols_map

CHN_PUNCTUATION_MAPPING = {
  "。": ".",
  "？": "?",
  "！": "!",
  "，": ",",
  "：": ":",
  "；": ";",
  "「": "\"",
  "」": "\"",
  "『": "\"",
  "』": "\"",
  "、": ",",
}

CHN_PUNCTUATION: Set[Symbol] = set(CHN_PUNCTUATION_MAPPING.keys()) | set(string.punctuation)


def split_into_ipa_and_tones(word: str) -> Tuple[str, str]:
  word_ipa = ""
  word_tones = ""
  for character in word:
    if character in TONES:
      word_tones += character
    else:
      word_ipa += character
  return word_ipa, word_tones


def is_vowel(symbol: Symbol) -> bool:
  vowels = VOWELS | SCHWAS
  result = all(sub_symbol in vowels for sub_symbol in tuple(symbol))
  return result


def get_vowel_count(symbols: Symbols) -> int:
  result = sum(1 if is_vowel(symbol) else 0 for symbol in symbols)
  return result


def __get_chn_ipa(word: Symbols) -> Symbols:
  # e.g. -> 北风 = peɪ˧˩˧ fɤ˥ŋ
  assert isinstance(word, tuple)
  assert len(word) > 0

  word_str = ''.join(word)
  syllable_split_symbol = " "
  hanzi_ipa = hanzi.to_ipa(word_str, delimiter=syllable_split_symbol)
  hanzi_syllables_ipa = hanzi_ipa.split(syllable_split_symbol)
  word_ipa_symbols = []
  for hanzi_syllable_ipa in hanzi_syllables_ipa:
    syllable_ipa, tone_ipa = split_into_ipa_and_tones(hanzi_syllable_ipa)
    assert hanzi_syllable_ipa.endswith(tone_ipa)
    syllable_ipa_symbols = parse_ipa_to_symbols(syllable_ipa)
    syllable_vowel_count = get_vowel_count(syllable_ipa_symbols)
    assert tone_ipa == "" or syllable_vowel_count == 1
    if syllable_vowel_count == 0:
      assert hanzi_syllable_ipa == "ɻ"
    syllable_ipa_symbols_with_tones = tuple(
      symbol + tone_ipa if is_vowel(symbol) else symbol for symbol in syllable_ipa_symbols)
    word_ipa_symbols.extend(syllable_ipa_symbols_with_tones)
  symbols = tuple(word_ipa_symbols)
  return symbols


def chn_to_ipa(chn_sentence: Symbols, consider_annotations: bool, annotation_split_symbol: Optional[Symbol]) -> Symbols:
  symbols = sentence2pronunciation_cached(
    sentence=chn_sentence,
    annotation_split_symbol=annotation_split_symbol,
    consider_annotation=consider_annotations,
    get_pronunciation=__get_chn_ipa,
    split_on_hyphen=False,
    trim_symbols=CHN_PUNCTUATION,
    ignore_case_in_cache=True,
  )

  symbols = symbols_map(symbols, CHN_PUNCTUATION_MAPPING)
  return symbols
