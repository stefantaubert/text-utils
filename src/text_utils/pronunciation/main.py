import string
from enum import Enum
from functools import partial
from logging import WARNING, getLogger
from typing import Dict, Optional, Set, Tuple

from ordered_set import OrderedSet
from pronunciation_dict_parser import PronunciationDict
from sentence2pronunciation import (clear_cache, get_non_annotated_words,
                                    sentence2pronunciation_cached)
from text_utils.language import Language
from text_utils.pronunciation.ARPAToIPAMapper import symbols_map_arpa_to_ipa
from text_utils.pronunciation.chinese_ipa import chn_to_ipa
from text_utils.pronunciation.epitran_cache import (get_eng_epitran,
                                                    get_ger_epitran)
from text_utils.pronunciation.G2p_cache import get_eng_g2p
from text_utils.pronunciation.ipa2symb import add_n_thongs
from text_utils.pronunciation.ipa2symb import \
    break_n_thongs as break_n_thongs_method
from text_utils.pronunciation.ipa2symb import (merge_template, merge_together,
                                               parse_ipa_symbols_to_symbols,
                                               parse_ipa_to_symbols,
                                               remove_arcs, remove_stress,
                                               remove_tones)
from text_utils.pronunciation.ipa_symbols import (ENG_ARPA_DIPHTONGS,
                                                  PUNCTUATION_AND_WHITESPACE,
                                                  TIES)
from text_utils.pronunciation.pronunciation_dict_cache import \
    get_eng_pronunciation_dict
from text_utils.symbol_format import SymbolFormat
from text_utils.types import Symbol, Symbols
from text_utils.utils import symbols_to_upper

DEFAULT_IGNORE_PUNCTUATION: Set[Symbol] = set(string.punctuation)
DEFAULT_PUNCTUATION_FOR_SPACE_REMOVAL: Set[Symbol] = {".", ",", ";", "?", "!"}
ANNOTATION_SPLIT_SYMBOL: Symbol = "/"


def clear_ipa_cache():
  clear_cache()


def clear_arpa_cache():
  clear_cache()


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
  word_ipa_symbols_str = epi_instance.transliterate(word_str)

  main_logger.setLevel(old_level)

  word_ipa_symbols = parse_ipa_to_symbols(word_ipa_symbols_str)

  # symbols = tuple(symbols_str)
  # symbols = merge_together(
  #   symbols=symbols,
  #   merge_symbols=TIES,
  #   ignore_merge_symbols=PUNCTUATION_AND_WHITESPACE,
  # )

  # symbols_contain_no_arpa_diphtongs = len(ENG_ARPA_DIPHTONGS.intersection(set(symbols))) == 0
  # assert symbols_contain_no_arpa_diphtongs
  # assert parse_ipa_to_symbols(symbols_str) == symbols

  return word_ipa_symbols


def __get_ger_ipa(word: Symbols) -> Symbols:
  assert isinstance(word, tuple)
  main_logger = getLogger()
  old_level = main_logger.level
  main_logger.setLevel(WARNING)

  epi_instance = get_ger_epitran()
  word_str = ''.join(word)
  word_ipa_symbols_str = epi_instance.transliterate(word_str)

  main_logger.setLevel(old_level)

  word_ipa_symbols = parse_ipa_to_symbols(word_ipa_symbols_str)
  return word_ipa_symbols


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
  mapped_ipa_str = ''.join(result_ipa)
  reparsed_ipa = parse_ipa_to_symbols(mapped_ipa_str)
  # if reparsed_ipa != result_ipa:
  #   logger = getLogger(__name__)
  #   logger.info(f"Changed parsing of \"{' '.join(result_ipa)}\" to \"{' '.join(reparsed_ipa)}\".")

  # assert parse_ipa_to_symbols(''.join(result_ipa)) == result_ipa
  # result_ipa = parse_ipa_symbols_to_symbols(result_ipa)

  return reparsed_ipa


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


def log_and_return_exception(msg: str) -> Exception:
  logger = getLogger(__name__)
  logger.exception(msg)
  return Exception(msg)


def symbols_to_ipa(symbols: Symbols, symbols_format: SymbolFormat, lang: Language, mode: Optional[EngToIPAMode], consider_annotations: Optional[bool]) -> Tuple[Symbols, SymbolFormat]:
  if symbols_format.is_IPA:
    return symbols, symbols_format
  if symbols_format == SymbolFormat.PHONEMES_ARPA:
    raise log_and_return_exception("Not supported!")
  assert symbols_format == SymbolFormat.GRAPHEMES

  if consider_annotations is None:
    raise log_and_return_exception("Please specify 'consider_annotations'.")

  if lang == Language.ENG:
    if mode is None:
      raise log_and_return_exception("Please specify the IPA conversion mode.")
    new_symbols = eng_to_ipa(symbols, consider_annotations, mode=mode)
    return new_symbols, SymbolFormat.PHONEMES_IPA
  if lang == Language.GER:
    new_symbols = ger_to_ipa(symbols, consider_annotations)
    return new_symbols, SymbolFormat.PHONEMES_IPA
  if lang == Language.CHN:
    new_symbols = chn_to_ipa(symbols, consider_annotations, ANNOTATION_SPLIT_SYMBOL)
    return new_symbols, SymbolFormat.PHONEMES_IPA
  assert False


def symbols_to_arpa(symbols: Symbols, symbols_format: SymbolFormat, lang: Language, consider_annotations: Optional[bool]) -> Tuple[Symbols, SymbolFormat]:
  if symbols_format == SymbolFormat.PHONEMES_ARPA:
    return symbols, symbols_format
  if symbols_format.is_IPA:
    raise log_and_return_exception("Not supported!")
  assert symbols_format == SymbolFormat.GRAPHEMES

  if consider_annotations is None:
    raise log_and_return_exception("Please specify 'consider_annotations'.")

  if lang in (Language.GER, Language.CHN):
    raise log_and_return_exception("Language is not supported!")

  if lang == Language.ENG:
    new_symbols = eng_to_arpa(symbols, consider_annotations)
    return new_symbols, SymbolFormat.PHONEMES_ARPA

  assert False


def change_ipa(symbols: Symbols, ignore_tones: bool, ignore_arcs: bool, ignore_stress: bool, break_n_thongs: bool, build_n_thongs: bool) -> Symbols:
  new_symbols = symbols

  if ignore_arcs:
    new_symbols = remove_arcs(new_symbols)

  if ignore_tones:
    new_symbols = remove_tones(new_symbols)

  if ignore_stress:
    new_symbols = remove_stress(new_symbols)

  if break_n_thongs:
    new_symbols = break_n_thongs_method(new_symbols)

  if build_n_thongs:
    new_symbols = add_n_thongs(symbols)

  return new_symbols


def symbols_to_arpa_pronunciation_dict(symbols: Symbols, symbols_format: SymbolFormat, language: Language, ignore_case: bool, split_on_hyphen: bool, consider_annotations: bool) -> PronunciationDict:
  # consider_annotations: if true then the annotations will be figured out and not taken into the dictionary. if false the annotations including the split symbol will be considered
  words = get_non_annotated_words(
    sentence=symbols,
    trim_symbols=DEFAULT_IGNORE_PUNCTUATION,
    consider_annotation=consider_annotations,
    annotation_split_symbol=ANNOTATION_SPLIT_SYMBOL,
    ignore_case=ignore_case,
    split_on_hyphen=split_on_hyphen,
  )

  result = {}
  for word in words:
    ipa_symbols, _ = symbols_to_arpa(
      symbols=word,
      symbols_format=symbols_format,
      lang=language,
      consider_annotations=False,
    )
    word_str = "".join(word)
    assert word_str not in result
    result[word_str] = OrderedSet([ipa_symbols])
  return result


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
