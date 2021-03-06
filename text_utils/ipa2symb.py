import string
from dataclasses import dataclass
from logging import Logger
from typing import List, Tuple

from ipapy.ipastring import IPAString

# _rx = '[{}]'.format(re.escape(string.punctuation))

ARC = '͡'


@dataclass
class IPAExtractionSettings():
  ignore_tones: bool
  ignore_arcs: bool
  replace_unknown_ipa_by: str


def check_is_ipa_and_return_closest_ipa(word_ipa: str) -> Tuple[bool, str]:
  try:
    ipa = IPAString(unicode_string=word_ipa, ignore=False)
    return True, ipa
  except ValueError:
    ipa = IPAString(unicode_string=word_ipa, ignore=True)
    return False, ipa


def extract_from_sentence(ipa_sentence: str, settings: IPAExtractionSettings, logger: Logger):
  res = []
  tmp: List[str] = []

  for c in ipa_sentence:
    if c in string.punctuation or c in string.whitespace:
      if len(tmp) > 0:
        raw_word_symbols = _extract_symbols(tmp, settings, logger)
        res.extend(raw_word_symbols)
        tmp.clear()
      res.append(c)
    else:
      tmp.append(c)

  if len(tmp) > 0:
    raw_word_symbols = _extract_symbols(tmp, settings, logger)
    res.extend(raw_word_symbols)
    tmp.clear()
  return res


def _extract_symbols(input_symbols: List[str], settings: IPAExtractionSettings, logger: Logger) -> List[str]:
  symbols: List[str] = []
  input_word = ''.join(input_symbols)
  is_valid_ipa, ipa = check_is_ipa_and_return_closest_ipa(input_word)
  if not is_valid_ipa:
    result = [settings.replace_unknown_ipa_by] * len(input_symbols)
    logger.info(
      f"Conversion of '{input_word}' to IPA failed. Result would be: '{ipa}'. Replaced with '{''.join(result)}' instead.")
    # TODO: Conversion of 'ðӕ' to IPA failed. Result would be: 'ð'. Replaced with '__' instead.
    return result

  for char in ipa.ipa_chars:
    if char.is_diacritic or char.is_tone:
      if len(symbols) > 0:
        if char.is_tone and settings.ignore_tones:
          continue
        # I think it is a bug in IPAString that the arc sometimes gets classified as diacritic and sometimes not
        if char.unicode_repr == ARC:
          if settings.ignore_arcs:
            continue
          symbols.append(ARC)
        else:
          symbols[-1] += char.unicode_repr
    else:
      uc = char.unicode_repr
      if settings.ignore_arcs:
        uc = uc.split(ARC)
        symbols.extend(uc)
      else:
        symbols.append(uc)

  return symbols
