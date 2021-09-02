from logging import getLogger
from typing import Dict

from epitran import Epitran

EPITRAN_ENG = 'eng-Latn'
EPITRAN_GER = 'deu-Latn'

EPITRAN_CACHE: Dict[str, Epitran] = {}


def get_eng_epitran() -> Epitran:
  # pylint: disable=global-statement
  global EPITRAN_CACHE
  ensure_eng_epitran_is_loaded()
  return EPITRAN_CACHE[EPITRAN_ENG]


def get_ger_epitran() -> Epitran:
  # pylint: disable=global-statement
  global EPITRAN_CACHE
  ensure_eng_epitran_is_loaded()
  return EPITRAN_CACHE[EPITRAN_GER]


def ensure_eng_epitran_is_loaded() -> None:
  # pylint: disable=global-statement
  global EPITRAN_CACHE
  if EPITRAN_ENG not in EPITRAN_CACHE.keys():
    logger = getLogger()
    logger.info("Loading English Epitran...")
    EPITRAN_CACHE[EPITRAN_ENG] = Epitran(EPITRAN_ENG)
    logger.info("Done.")


def ensure_ger_epitran_is_loaded() -> None:
  # pylint: disable=global-statement
  global EPITRAN_CACHE
  if EPITRAN_GER not in EPITRAN_CACHE.keys():
    logger = getLogger()
    logger.info("Loading German Epitran...")
    EPITRAN_CACHE[EPITRAN_GER] = Epitran(EPITRAN_GER)
    logger.info("Done.")
