import string
from enum import Enum
from functools import partial
from logging import WARNING, getLogger
from typing import Dict, Optional, Set, Tuple

from dragonmapper import hanzi
from sentence2pronunciation import clear_cache, sentence2pronunciation_cached
from text_utils.language import Language
from text_utils.pronunciation.ARPAToIPAMapper import symbols_map_arpa_to_ipa
from text_utils.pronunciation.epitran_cache import (get_eng_epitran,
                                                    get_ger_epitran)
from text_utils.pronunciation.G2p_cache import get_eng_g2p
from text_utils.pronunciation.ipa2symb import parse_ipa_to_symbols
from text_utils.pronunciation.pronunciation_dict_cache import \
    get_eng_pronunciation_dict
from text_utils.symbol_format import SymbolFormat
from text_utils.types import Symbol, Symbols
from text_utils.utils import symbols_to_upper


def clear_ipa_cache():
  clear_cache()


DEFAULT_IGNORE_PUNCTUATION: Set[Symbol] = set(string.punctuation)
ANNOTATION_SPLIT_SYMBOL = "/"


def __get_arpa_oov(word: Symbols) -> Symbols:
  model = get_eng_g2p()
  word_str = ''.join(word)
  oov_arpa = model.predict(word_str)
  logger = getLogger(__name__)
  logger.info(f"Transliterated OOV word \"{word_str}\" to \"{' '.join(oov_arpa)}\".")
  return oov_arpa


def lookup_dict(word: Symbols, dictionary: Dict[Symbols, Symbols]) -> Symbols:
  word_upper = symbols_to_upper(word)
  if word_upper in dictionary:
    return dictionary[word_upper][0]
  return __get_arpa_oov(word)


def eng_to_arpa(eng_sentence: Symbols, consider_annotations: bool) -> Symbols:
  pronunciations = get_eng_pronunciation_dict()
  method = partial(lookup_dict, dictionary=pronunciations)

  result = sentence2pronunciation_cached(
    sentence=eng_sentence,
    annotation_split_symbol=ANNOTATION_SPLIT_SYMBOL,
    consider_annotation=consider_annotations,
    get_pronunciation=method,
    split_on_hyphen=True,
    trim_symbols=DEFAULT_IGNORE_PUNCTUATION,
    ignore_case_in_cache=True,
  )

  return result


def __get_eng_ipa(word: Symbols) -> Symbols:
  assert isinstance(word, tuple)
  main_logger = getLogger()
  old_level = main_logger.level
  main_logger.setLevel(WARNING)

  epi_instance = get_eng_epitran()
  word_str = ''.join(word)
  result = epi_instance.transliterate(word_str)

  main_logger.setLevel(old_level)

  result_tuple = parse_ipa_to_symbols(result)
  return result_tuple


def __get_ger_ipa(word: Symbols) -> Symbols:
  assert isinstance(word, tuple)
  main_logger = getLogger()
  old_level = main_logger.level
  main_logger.setLevel(WARNING)

  epi_instance = get_ger_epitran()
  word_str = ''.join(word)
  result = epi_instance.transliterate(word_str)

  main_logger.setLevel(old_level)

  result_tuple = parse_ipa_to_symbols(result)
  return result_tuple


def eng_to_ipa_epitran(eng_sentence: Symbols, consider_annotations: bool) -> Symbols:
  #pronunciations = parse_public_dict(PublicDictType.MFA_EN_US_IPA)
  result = sentence2pronunciation_cached(
    sentence=eng_sentence,
    annotation_split_symbol=ANNOTATION_SPLIT_SYMBOL,
    consider_annotation=consider_annotations,
    get_pronunciation=__get_eng_ipa,
    split_on_hyphen=True,
    trim_symbols=DEFAULT_IGNORE_PUNCTUATION,
    ignore_case_in_cache=True,
  )

  return result


def eng_to_ipa_pronunciation_dict(eng_sentence: Symbols, consider_annotations: bool) -> Symbols:
  #pronunciations = parse_public_dict(PublicDictType.MFA_EN_US_IPA)
  arpa_symbols = eng_to_arpa(eng_sentence, consider_annotations)
  result_ipa = symbols_map_arpa_to_ipa(arpa_symbols, ignore={},
                                       replace_unknown=False, replace_unknown_with=None)

  return result_ipa


class EngToIPAMode(Enum):
  LIBRISPEECH = 0
  EPITRAN = 1


def eng_to_ipa(eng_sentence: Symbols, consider_annotations: bool, mode: EngToIPAMode) -> Symbols:
  if mode == EngToIPAMode.EPITRAN:
    return eng_to_ipa_epitran(eng_sentence, consider_annotations)
  if mode == EngToIPAMode.LIBRISPEECH:
    return eng_to_ipa_pronunciation_dict(eng_sentence, consider_annotations)
  assert False


def ger_to_ipa(ger_sentence: Symbols, consider_annotations: bool) -> Symbols:
  #pronunciations = parse_public_dict(PublicDictType.MFA_EN_US_IPA)
  result = sentence2pronunciation_cached(
    sentence=ger_sentence,
    annotation_split_symbol=ANNOTATION_SPLIT_SYMBOL,
    consider_annotation=consider_annotations,
    get_pronunciation=__get_ger_ipa,
    split_on_hyphen=True,
    trim_symbols=DEFAULT_IGNORE_PUNCTUATION,
    ignore_case_in_cache=True,
  )

  return result


def __get_chn_ipa(word: Symbols) -> Symbols:
  # e.g. -> 北风 = peɪ˧˩˧ fɤŋ˥
  assert isinstance(word, tuple)
  word_str = ''.join(word)
  chn_ipa = hanzi.to_ipa(word_str)
  # TODO move tones to vowels/diphtongs
  ipa_symbols = parse_ipa_to_symbols(chn_ipa)
  return ipa_symbols


def chn_to_ipa(chn_sentence: Symbols, consider_annotations: bool) -> Symbols:
  #pronunciations = parse_public_dict(PublicDictType.MFA_EN_US_IPA)
  result = sentence2pronunciation_cached(
    sentence=chn_sentence,
    annotation_split_symbol=ANNOTATION_SPLIT_SYMBOL,
    consider_annotation=consider_annotations,
    get_pronunciation=__get_chn_ipa,
    split_on_hyphen=True,
    trim_symbols=DEFAULT_IGNORE_PUNCTUATION,
    ignore_case_in_cache=True,
  )

  return result


def log_and_return_exception(msg: str) -> Exception:
  logger = getLogger(__name__)
  logger.exception(msg)
  return Exception(msg)


def symbols_to_ipa(symbols: Symbols, symbols_format: SymbolFormat, lang: Language, mode: Optional[EngToIPAMode], consider_ipa_annotations: Optional[bool]) -> Tuple[Symbols, SymbolFormat]:
  if symbols_format.is_IPA:
    return symbols, symbols_format
  if symbols_format == SymbolFormat.PHONEMES_ARPA:
    raise log_and_return_exception("Not supported!")
  assert symbols_format == SymbolFormat.GRAPHEMES

  if consider_ipa_annotations is None:
    raise log_and_return_exception("Please specify 'consider_ipa_annotations'.")

  if lang == Language.ENG:
    if mode is None:
      raise log_and_return_exception("Please specify the IPA conversion mode.")
    new_symbols = eng_to_ipa(symbols, consider_ipa_annotations, mode=mode)
    return new_symbols, SymbolFormat.PHONEMES_IPA
  if lang == Language.GER:
    new_symbols = ger_to_ipa(symbols, consider_ipa_annotations)
    return new_symbols, SymbolFormat.PHONEMES_IPA
  if lang == Language.CHN:
    new_symbols = chn_to_ipa(symbols, consider_ipa_annotations)
    return new_symbols, SymbolFormat.PHONEMES_IPA
  assert False


# def merge_symbols(pronunciation: Symbols, merge_at: Symbol, merge_on_symbols: Set[Symbol]) -> Symbols:
#   subsets, _ = split_symbols(pronunciation, split_on_symbols={merge_at})
#   merged_subsets = [merge_symbols_pronunciation(subset, merge_on_symbols) for subset in subsets]
#   result = join_pronunciations(merged_subsets, merge_at)
#   return result


# def split_symbols(symbols: Symbols, split_on_symbols: Set[Symbol]) -> Tuple[List[Symbols], List[Symbol]]:
#   result = []
#   current = []
#   splitted_on = []
#   for symbol in symbols:
#     if symbol in split_on_symbols:
#       splitted_on.append(symbol)
#       if len(current) > 0:
#         result.append(tuple(current))
#         current.clear()
#     else:
#       result.append(symbol)

#   if len(current) > 0:
#     result.append(tuple(current))
#     current.clear()

#   return result, splitted_on


# def join_pronunciations(pronunciations: List[Symbols], join_symbol: Symbol) -> Symbols:
#   result = []
#   for i, subset in enumerate(pronunciations):
#     result.extend(list(subset))
#     if i < len(pronunciations) - 1:
#       result.append(join_symbol)
#   return tuple(result)


# def merge_symbols_pronunciation(pronunciation: Symbols, merge_on_symbols: Set[Symbol]) -> Symbols:
#   if len(pronunciation) == 0:
#     return tuple()
#   if len(merge_on_symbols) == 0:
#     return pronunciation
#   # TODO consider: cat-o-nine-tails
#   merge_symbols_from_start = []
#   for symbol in pronunciation:
#     if symbol in merge_on_symbols:
#       merge_symbols_from_start.append(symbol)

#   merge_symbols_from_end = []
#   for symbol in pronunciation[::-1]:
#     if symbol in merge_on_symbols:
#       merge_symbols_from_end.append(symbol)
#   merge_symbols_from_end = merge_symbols_from_end[::-1]

#   complete_pronun_has_only_merge_symbols = len(merge_symbols_from_start) == len(pronunciation)
#   if complete_pronun_has_only_merge_symbols:
#     return (''.join(merge_symbols_from_start),)

#   return pronunciation
