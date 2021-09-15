from typing import Dict

from pronunciation_dict_parser import (PronunciationDict, PublicDictType,
                                       parse_public_dict)
from text_utils.types import Symbols
from text_utils.utils import pronunciation_dict_to_tuple_dict

CACHE: Dict[Symbols, Symbols] = None


def get_eng_pronunciation_dict() -> PronunciationDict:
  # pylint: disable=global-statement
  global CACHE
  if CACHE is None:
    arpa_dict = parse_public_dict(PublicDictType.LIBRISPEECH_ARPA)
    arpa_dict_tuple_based = pronunciation_dict_to_tuple_dict(arpa_dict)
    CACHE = arpa_dict_tuple_based
  return CACHE
