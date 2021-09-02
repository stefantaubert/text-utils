from pronunciation_dict_parser import PublicDictType, parse_public_dict
from pronunciation_dict_parser import PronunciationDict

CACHE: PronunciationDict = None


def get_eng_pronunciation_dict() -> PronunciationDict:
  # pylint: disable=global-statement
  global CACHE
  if CACHE is None:
    CACHE = parse_public_dict(PublicDictType.LIBRISPEECH_ARPA)
  return CACHE
