from logging import WARNING, Logger, getLogger
from typing import Dict

from epitran import Epitran

from text_utils.ipa2symb import (ipa_of_phonetic_transcription,
                                 is_phonetic_transcription,
                                 is_phonetic_transcription_in_text)
from text_utils.language import Language

EPITRAN_CACHE: Dict[Language, Epitran] = {}
EPITRAN_EN_WORD_CACHE: Dict[str, str] = {}


def en_to_ipa_epitran(text: str, logger: Logger, use_cache: bool = True) -> str:
  global EPITRAN_CACHE

  ensure_eng_epitran_is_loaded(logger)

  if use_cache:
    splitted_text = text.split(" ")
    splitted_result = [epi_transliterate_word_cached_verbose(
      word, logger, verbose=False) for word in splitted_text]
    result = " ".join(splitted_result)
    return result
  result = epi_transliterate_without_logging(EPITRAN_CACHE[Language.ENG], text)
  return result


def ensure_eng_epitran_is_loaded(logger: Logger) -> None:
  global EPITRAN_CACHE
  if Language.ENG not in EPITRAN_CACHE.keys():
    logger.info("Loading English Epitran...")
    EPITRAN_CACHE[Language.ENG] = Epitran('eng-Latn')


def ensure_ger_epitran_is_loaded(logger: Logger) -> None:
  global EPITRAN_CACHE
  if Language.GER not in EPITRAN_CACHE.keys():
    logger.info("Loading German Epitran...")
    EPITRAN_CACHE[Language.GER] = Epitran('deu-Latn')


def epi_transliterate_word_cached_verbose(word: str, logger: Logger, verbose: bool = True) -> str:
  # I am assuming there is no IPA difference in EPITRAN.
  word = word.lower()

  if word in EPITRAN_EN_WORD_CACHE:
    return EPITRAN_EN_WORD_CACHE[word]

  res = epi_transliterate_word_verbose(word, logger, verbose)

  EPITRAN_EN_WORD_CACHE[word] = res

  return res


def epi_transliterate_word_verbose(word: str, logger: Logger, verbose: bool = True) -> str:
  global EPITRAN_CACHE
  assert Language.ENG in EPITRAN_CACHE

  res = epi_transliterate_without_logging(EPITRAN_CACHE[Language.ENG], word)
  # res = EPITRAN_CACHE[Language.ENG].transliterate(word)

  if verbose:
    logger.info(f"used Epitran for: {word} => {res}")

  return res


def epi_transliterate_without_logging(epi_instance: Epitran, word: str) -> str:
  main_logger = getLogger()
  old_level = main_logger.level
  main_logger.setLevel(WARNING)

  result = epi_instance.transliterate(word)

  main_logger.setLevel(old_level)

  return result


def ger_to_ipa(text: str, consider_ipa_annotations: bool, logger: Logger) -> str:
  if consider_ipa_annotations and is_phonetic_transcription_in_text(text):
    words = text.split(" ")
    ipa_list = [ipa_of_phonetic_transcription(word, logger)
                if is_phonetic_transcription(word)
                else ger_ipa_of_text_not_containing_phonetic_transcription(text=word, logger=logger)
                for word in words]
    res = " ".join(ipa_list)
    return res
  return ger_ipa_of_text_not_containing_phonetic_transcription(text, logger)


def ger_ipa_of_text_not_containing_phonetic_transcription(text: str, logger: Logger) -> str:
  global EPITRAN_CACHE
  ensure_ger_epitran_is_loaded(logger)
  result = epi_transliterate_without_logging(EPITRAN_CACHE[Language.GER], text)
  # result = EPITRAN_CACHE[Language.GER].transliterate(text)
  return result


def clear_en_word_cache() -> None:
  EPITRAN_EN_WORD_CACHE.clear()
