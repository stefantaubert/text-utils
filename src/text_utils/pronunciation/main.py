import string
from logging import WARNING, Logger, getLogger
from typing import Optional, Set, Tuple

from dragonmapper import hanzi
from pronunciation_dict_parser import PublicDictType, parse_public_dict
from text_utils.language import Language
from text_utils.pronunciation.dummy_text2pronunciation import (
    sentence2pronunciaton, sentence2pronunciaton2)
from text_utils.pronunciation.epitran_cache import (get_eng_epitran,
                                                    get_ger_epitran)
from text_utils.pronunciation.G2p_cache import get_eng_g2p
from text_utils.pronunciation.pronunciation_dict_cache import \
    get_eng_pronunciation_dict

Symbol = str
Pronunciation = Tuple[Symbol, ...]


def __get_arpa_oov(word: str) -> Pronunciation:
  model = get_eng_g2p()
  result = model.predict(word)
  logger = getLogger(__name__)
  logger.info(f"Transliterated OOV word \"{word}\" to \"{''.join(result)}\".")
  return result

def eng_to_arpa(eng_sentence: str, consider_annotations: bool) -> Pronunciation:
  pronunciations = get_eng_pronunciation_dict()
  result = sentence2pronunciaton(
    sentence=eng_sentence,
    dictionary=pronunciations,
    annotation_indicator="/",
    consider_annotations=consider_annotations,
    replace_unknown_with=__get_arpa_oov,
    split_on_hyphen=True,
    trim_symb=set(string.punctuation),
    use_cache=True,
    ignore_case_in_cache=True,
  )

  return result


def __get_eng_ipa(word: str) -> Pronunciation:
  main_logger = getLogger()
  old_level = main_logger.level
  main_logger.setLevel(WARNING)

  epi_instance = get_eng_epitran()
  result = epi_instance.transliterate(word)

  main_logger.setLevel(old_level)

  result_tuple = tuple(result)
  return result_tuple


def __get_ger_ipa(word: str) -> Pronunciation:
  main_logger = getLogger()
  old_level = main_logger.level
  main_logger.setLevel(WARNING)

  epi_instance = get_ger_epitran()
  result = epi_instance.transliterate(word)

  main_logger.setLevel(old_level)

  result_tuple = tuple(result)
  return result_tuple


def eng_to_ipa(eng_sentence: str, consider_annotations: bool) -> Pronunciation:
  #pronunciations = parse_public_dict(PublicDictType.MFA_EN_US_IPA)
  result = sentence2pronunciaton2(
    sentence=eng_sentence,
    annotation_indicator="/",
    consider_annotations=consider_annotations,
    lookup=__get_eng_ipa,
    split_on_hyphen=True,
    trim_symb=set(string.punctuation),
    use_cache=True,
    ignore_case_in_cache=True,
  )

  return result


def ger_to_ipa(ger_sentence: str, consider_annotations: bool) -> Pronunciation:
  #pronunciations = parse_public_dict(PublicDictType.MFA_EN_US_IPA)
  result = sentence2pronunciaton2(
    sentence=ger_sentence,
    annotation_indicator="/",
    consider_annotations=consider_annotations,
    lookup=__get_ger_ipa,
    split_on_hyphen=True,
    trim_symb=set(string.punctuation),
    use_cache=True,
    ignore_case_in_cache=True,
  )

  return result


def __get_chn_ipa(word: str) -> Pronunciation:
  chn_ipa = hanzi.to_ipa(word)
  ipa_symbols = tuple(chn_ipa.split(" "))
  return ipa_symbols


def chn_to_ipa(chn_sentence: str, consider_annotations: bool) -> Pronunciation:
  #pronunciations = parse_public_dict(PublicDictType.MFA_EN_US_IPA)
  result = sentence2pronunciaton2(
    sentence=chn_sentence,
    annotation_indicator="/",
    consider_annotations=consider_annotations,
    lookup=__get_chn_ipa,
    split_on_hyphen=True,
    trim_symb=set(string.punctuation),
    use_cache=False,
  )

  return result


def ignore_symbols(symbols: Pronunciation, ignore: Set[Symbol]) -> Pronunciation:
  res = tuple(symbol for symbol in symbols if symbol not in ignore)
  return res


def merge_symbols(pronunciation: Pronunciation, merge_at: Symbol, merge_symbols: Set[Symbol]) -> Pronunciation:
  return pronunciation
