import string
from enum import Enum
from logging import WARNING, getLogger
from typing import Optional, Tuple

from dragonmapper import hanzi
from text_utils.language import Language
from text_utils.pronunciation.ARPAToIPAMapper import symbols_map_arpa_to_ipa
from text_utils.pronunciation.dummy_text2pronunciation import (
    get_sentence2pronunciaton, get_sentence2pronunciaton2)
from text_utils.pronunciation.epitran_cache import (get_eng_epitran,
                                                    get_ger_epitran)
from text_utils.pronunciation.G2p_cache import get_eng_g2p
from text_utils.pronunciation.ipa2symb import parse_ipa_to_symbols
from text_utils.pronunciation.pronunciation_dict_cache import \
    get_eng_pronunciation_dict
from text_utils.symbol_format import SymbolFormat
from text_utils.types import Symbols

#IGONRE_PUNCTUATION = {".", ",", ";", "'", "\""}
IGONRE_PUNCTUATION = set(string.punctuation)


def __get_arpa_oov(word: str) -> Symbols:
  model = get_eng_g2p()
  result = model.predict(word)
  logger = getLogger(__name__)
  logger.info(f"Transliterated OOV word \"{word}\" to \"{''.join(result)}\".")
  return result


def eng_to_arpa(eng_sentence: str, consider_annotations: bool) -> Symbols:
  pronunciations = get_eng_pronunciation_dict()
  result = get_sentence2pronunciaton(
    sentence=eng_sentence,
    dictionary=pronunciations,
    annotation_indicator="/",
    consider_annotations=consider_annotations,
    replace_unknown_with=__get_arpa_oov,
    split_on_hyphen=True,
    trim_symb=IGONRE_PUNCTUATION,
    use_cache=True,
    ignore_case_in_cache=True,
  )

  return result


def __get_eng_ipa(word: str) -> Symbols:
  main_logger = getLogger()
  old_level = main_logger.level
  main_logger.setLevel(WARNING)

  epi_instance = get_eng_epitran()
  result = epi_instance.transliterate(word)

  main_logger.setLevel(old_level)

  result_tuple = tuple(result)
  return result_tuple


def __get_ger_ipa(word: str) -> Symbols:
  main_logger = getLogger()
  old_level = main_logger.level
  main_logger.setLevel(WARNING)

  epi_instance = get_ger_epitran()
  result = epi_instance.transliterate(word)

  main_logger.setLevel(old_level)

  result_tuple = tuple(result)
  return result_tuple


def eng_to_ipa_epitran(eng_sentence: str, consider_annotations: bool) -> Symbols:
  #pronunciations = parse_public_dict(PublicDictType.MFA_EN_US_IPA)
  result = get_sentence2pronunciaton2(
    sentence=eng_sentence,
    annotation_indicator="/",
    consider_annotations=consider_annotations,
    lookup=__get_eng_ipa,
    split_on_hyphen=True,
    trim_symb=IGONRE_PUNCTUATION,
    use_cache=True,
    ignore_case_in_cache=True,
  )

  return result


def eng_to_ipa_pronunciation_dict(eng_sentence: str, consider_annotations: bool) -> Symbols:
  #pronunciations = parse_public_dict(PublicDictType.MFA_EN_US_IPA)
  arpa_symbols = eng_to_arpa(eng_sentence, consider_annotations)
  result_ipa = symbols_map_arpa_to_ipa(arpa_symbols, ignore={},
                                       replace_unknown=False, replace_unknown_with=None)

  return result_ipa


class EngToIPAMode(Enum):
  LIBRISPEECH = 0
  EPITRAN = 1


def eng_to_ipa(eng_sentence: str, consider_annotations: bool, mode: EngToIPAMode) -> Symbols:
  if mode == EngToIPAMode.EPITRAN:
    return eng_to_ipa_epitran(eng_sentence, consider_annotations)
  elif mode == EngToIPAMode.LIBRISPEECH:
    return eng_to_ipa_pronunciation_dict(eng_sentence, consider_annotations)
  else:
    assert False


def ger_to_ipa(ger_sentence: str, consider_annotations: bool) -> Symbols:
  #pronunciations = parse_public_dict(PublicDictType.MFA_EN_US_IPA)
  result = get_sentence2pronunciaton2(
    sentence=ger_sentence,
    annotation_indicator="/",
    consider_annotations=consider_annotations,
    lookup=__get_ger_ipa,
    split_on_hyphen=True,
    trim_symb=IGONRE_PUNCTUATION,
    use_cache=True,
    ignore_case_in_cache=True,
  )

  return result


def __get_chn_ipa(word: str) -> Symbols:
  # e.g. -> 北风 = peɪ˧˩˧ fɤŋ˥
  chn_ipa = hanzi.to_ipa(word)
  ipa_symbols = parse_ipa_to_symbols(chn_ipa)
  return ipa_symbols


def chn_to_ipa(chn_sentence: str, consider_annotations: bool) -> Symbols:
  #pronunciations = parse_public_dict(PublicDictType.MFA_EN_US_IPA)
  result = get_sentence2pronunciaton2(
    sentence=chn_sentence,
    annotation_indicator="/",
    consider_annotations=consider_annotations,
    lookup=__get_chn_ipa,
    split_on_hyphen=True,
    trim_symb=IGONRE_PUNCTUATION,
    use_cache=False,
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

  text = ''.join(symbols)
  if lang == Language.ENG:
    if mode is None:
      raise log_and_return_exception("Please specify the IPA conversion mode.")
    new_symbols = eng_to_ipa(text, consider_ipa_annotations, mode=mode)
    return new_symbols, SymbolFormat.PHONEMES_IPA
  if lang == Language.GER:
    new_symbols = ger_to_ipa(text, consider_ipa_annotations)
    return new_symbols, SymbolFormat.PHONEMES_IPA
  if lang == Language.CHN:
    new_symbols = chn_to_ipa(text, consider_ipa_annotations)
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
