
from functools import partial
from logging import Logger
from typing import Optional

from cmudict_parser import CMUDict
from cmudict_parser.CMUDict import get_dict

from text_utils.epitran_wrapper import (ensure_eng_epitran_is_loaded,
                                        epi_transliterate_word_cached_verbose,
                                        epi_transliterate_word_verbose)

CMU_CACHE: Optional[CMUDict] = None


def ensure_cmudict_is_loaded(logger: Logger) -> None:
  global CMU_CACHE
  if CMU_CACHE is None:
    logger.info("Loading CMU dictionary...")
    CMU_CACHE = get_dict(silent=True)


def en_to_ipa_cmu_epitran(text: str, use_cache: bool, logger: Logger) -> str:
  global CMU_CACHE

  ensure_cmudict_is_loaded(logger)
  ensure_eng_epitran_is_loaded(logger)

  try:
    replacing_func = partial(epi_transliterate_word_cached_verbose, logger=logger) if use_cache else partial(
        epi_transliterate_word_verbose, logger=logger)

    result = CMU_CACHE.sentence_to_ipa(
      sentence=text,
      replace_unknown_with=replacing_func
    )
    return result
  except Exception as orig_exception:
    ex = ValueError(f"Conversion of '{text}' was not successfull!")
    logger.error("", exc_info=ex)
    raise ex from orig_exception


def en_to_ipa_cmu(text: str, replace_unknown_with: str, logger: Logger) -> str:
  assert replace_unknown_with is not None
  global CMU_CACHE

  ensure_cmudict_is_loaded(logger)

  try:
    result = CMU_CACHE.sentence_to_ipa(
      sentence=text,
      replace_unknown_with=replace_unknown_with
    )
    return result
  except Exception as orig_exception:
    ex = ValueError(f"Conversion of '{text}' was not successfull!")
    logger.error("", exc_info=ex)
    raise ex from orig_exception
