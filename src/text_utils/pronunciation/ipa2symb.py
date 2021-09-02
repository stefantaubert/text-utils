import re
import string
from dataclasses import dataclass
from logging import Logger, getLogger
from typing import List, Optional, Tuple

from ipapy.ipachar import IPAChar
from ipapy.ipastring import IPAString

# _rx = '[{}]'.format(re.escape(string.punctuation))

ARC = '͡'

STRESS_SYMBOLS = {"ˌ", "ˈ"}
SLASH = re.compile(r'/')


WHOLE_STRING_IS_PHONETIC_TRANS = re.compile(r'\A/\S*/\Z')
PH_TRANS = re.compile(r'/(\S*)/')


def is_phonetic_transcription_in_text(text: str) -> bool:
  #ph_trans_in_text = PH_TRANS_NO_WHITESPACE.match(text)
  ph_trans_in_text = PH_TRANS.search(text)
  return ph_trans_in_text is not None


def is_phonetic_transcription(text: str) -> bool:
  ipa_of_ph_trans = WHOLE_STRING_IS_PHONETIC_TRANS.search(text)
  return ipa_of_ph_trans is not None


@dataclass
class IPAExtractionSettings():
  ignore_tones: bool
  ignore_arcs: bool
  replace_unknown_ipa_by: str


def ipa_of_phonetic_transcription(ph_trans: str, logger: Logger) -> str:
  assert is_phonetic_transcription(ph_trans)
  resulting_ipa = re.sub(SLASH, '', ph_trans)
  is_ipa, _ = check_is_ipa_and_return_closest_ipa(resulting_ipa)
  if not is_ipa:
    ex = ValueError(f"'{ph_trans}': '{resulting_ipa}' is no valid IPA!")
    logger.error("", exc_info=ex)
    raise ex
  return resulting_ipa


def check_is_ipa_and_return_closest_ipa(word_ipa: str) -> Tuple[bool, IPAString]:
  try:
    ipa = IPAString(unicode_string=word_ipa, ignore=False)
    return True, ipa
  except ValueError:
    ipa = IPAString(unicode_string=word_ipa, ignore=True)
    return False, ipa


def extract_from_sentence(ipa_sentence: str, settings: IPAExtractionSettings, merge_stress: bool) -> List[str]:
  res: List[str] = []
  tmp: List[str] = []

  for c in ipa_sentence:
    if c in string.punctuation or c in string.whitespace:
      if len(tmp) > 0:
        raw_word_symbols = _extract_symbols(tmp, settings, merge_stress)
        res.extend(raw_word_symbols)
        tmp.clear()
      res.append(c)
    else:
      tmp.append(c)

  if len(tmp) > 0:
    raw_word_symbols = _extract_symbols(tmp, settings, merge_stress)
    res.extend(raw_word_symbols)
    tmp.clear()
  return res


def _extract_symbols(input_symbols: List[str], settings: IPAExtractionSettings, merge_stress: bool) -> List[str]:
  input_word = ''.join(input_symbols)
  is_valid_ipa, ipa = check_is_ipa_and_return_closest_ipa(input_word)

  if not is_valid_ipa:
    logger = getLogger(__name__)
    result = [settings.replace_unknown_ipa_by] * len(input_symbols)
    logger.warning(
      f"Conversion of '{input_word}' to IPA failed. Result would be: '{ipa}'. Replaced with '{''.join(result)}' instead.")
    # TODO: Conversion of 'ðӕ' to IPA failed. Result would be: 'ð'. Replaced with '__' instead.
    return result

  return ipa_str_to_list(ipa, settings.ignore_tones, settings.ignore_arcs, merge_stress)


def ipa_str_to_list(ipa_str: IPAString, ignore_tones: bool, ignore_arcs: bool, merge_stress: bool) -> List[str]:
  symbols: List[str] = []

  tmp_stress: Optional[str] = None
  char: IPAChar
  for char in ipa_str.ipa_chars:
    char_is_stress = char.unicode_repr in STRESS_SYMBOLS
    if char_is_stress:
      if tmp_stress is not None:
        if merge_stress:
          tmp_stress = f"{tmp_stress}{char.unicode_repr}"
        else:
          symbols.append(tmp_stress)
          tmp_stress = char.unicode_repr
      else:
        tmp_stress = char.unicode_repr
      continue

    if char.is_diacritic or char.is_tone:
      if len(symbols) > 0:
        if char.is_tone and ignore_tones:
          continue
        # I think it is a bug in IPAString that the arc sometimes gets classified as diacritic and sometimes not
        if char.unicode_repr == ARC:
          if ignore_arcs:
            continue
          # symbols.append(ARC)
          symbols[-1] += char.unicode_repr
        else:
          symbols[-1] += char.unicode_repr
    else:
      uc = char.unicode_repr
      if ignore_arcs:
        extend_symbols = uc.split(ARC)
        if tmp_stress is not None:
          if merge_stress:
            extend_symbols[0] = f"{tmp_stress}{extend_symbols[0]}"
          else:
            extend_symbols = [tmp_stress] + extend_symbols
          tmp_stress = None
      else:
        extend_symbols = [uc]
        if tmp_stress is not None:
          if merge_stress:
            extend_symbols[0] = f"{tmp_stress}{extend_symbols[0]}"
          else:
            extend_symbols = [tmp_stress] + extend_symbols
          tmp_stress = None

      symbols.extend(extend_symbols)

  if tmp_stress is not None:
    symbols.append(tmp_stress)

  return symbols
