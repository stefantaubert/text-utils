import re
from typing import Iterable, List, Set, Tuple

from text_utils.pronunciation.ipa_symbols import (APPENDIX, DONT_CHANGE, MERGE,
                                                  PREPEND, STRESS_PRIMARY,
                                                  STRESS_SECONDARY, TIE_ABOVE,
                                                  TIE_BELOW, TONES)
from text_utils.types import Symbol, Symbols
from text_utils.utils import remove_symbols_at_all_places

# _rx = '[{}]'.format(re.escape(string.punctuation))
# https://www.internationalphoneticalphabet.org/ipa-charts/ipa-symbols-with-unicode-decimal-and-hex-codes/

# ARC = '͡'

# STRESS_SYMBOLS = {"ˌ", "ˈ"}
# SLASH = re.compile(r'/')

# TONE_SYMBOLS_HEX = {"030B", "0301", "0304", "0300", "030F"}
# ARCS_HEX = {"035C", "0361"}
# ASPIRATED_HEX = {"02B0"}
# STRESS_HEX = {"02C8", "02CC"}
# LENGTH_MARKS = {"02D0", "02D1"}
# SYLLABILIC = "0329"

# WHOLE_STRING_IS_PHONETIC_TRANS = re.compile(r'\A/\S*/\Z')
# PH_TRANS = re.compile(r'/(\S*)/')


# def hex_to_str(hex_number: str) -> str:
#   result = chr(int(hex_number, base=16))
#   return result


def remove_arcs(symbols: Symbols) -> Symbols:
  symbols = remove_symbols_at_all_places(symbols, ignore={TIE_ABOVE, TIE_BELOW})
  return symbols


def remove_tones(symbols: Symbols) -> Symbols:
  symbols = remove_symbols_at_all_places(symbols, ignore=TONES)
  return symbols


def remove_stress(symbols: Symbols) -> Symbols:
  symbols = remove_symbols_at_all_places(symbols, ignore={STRESS_PRIMARY, STRESS_SECONDARY})
  return symbols


def parse_ipa_to_symbols(sentence: str) -> Symbols:
  all_symbols = tuple(sentence)
  all_symbols = merge_together(all_symbols, merge_symbols=MERGE, ignore_merge_symbols=DONT_CHANGE)
  all_symbols = merge_left(all_symbols, merge_symbols=PREPEND, ignore_merge_symbols=DONT_CHANGE)
  all_symbols = merge_right(all_symbols, merge_symbols=APPENDIX, ignore_merge_symbols=DONT_CHANGE)
  return all_symbols


# def merge_together(symbols: Symbols, merge_symbols: Set[Symbol], ignore_merge_symbols: Set[Symbol]) -> Symbols:
#   merge_or_ignore_merge_symbols = merge_symbols.union(ignore_merge_symbols)
#   j = 0
#   merged_symbols = []
#   while j < len(symbols):
#     new_symbol = symbols[j]
#     j += 1
#     while symbols[j - 1] not in merge_or_ignore_merge_symbols and j < len(symbols):
#       merge_symbol_concat, index = get_all_next_merge_symbols(symbols[j:], merge_symbols)
#       if len(merge_symbol_concat) > 0 and symbols[j + index] not in merge_or_ignore_merge_symbols:
#         new_symbol += merge_symbol_concat + symbols[j + index]
#         j += index + 1
#       else:
#         break
#     merged_symbols.append(new_symbol)
#   return tuple(merged_symbols)

def merge_together(symbols: Symbols, merge_symbols: Set[Symbol], ignore_merge_symbols: Set[Symbol]) -> Symbols:
  merge_or_ignore_merge_symbols = merge_symbols.union(ignore_merge_symbols)
  j = 0
  merged_symbols = []
  while j < len(symbols):
    new_symbol, j = get_next_merged_together_symbol(
      symbols, j, merge_symbols, merge_or_ignore_merge_symbols)
    merged_symbols.append(new_symbol)
  return tuple(merged_symbols)


def get_next_merged_together_symbol(symbols: Symbols, j, merge_symbols: Set[Symbol], merge_or_ignore_merge_symbols: Set[Symbol]):
  new_symbol = symbols[j]
  j += 1
  while symbols[j - 1] not in merge_or_ignore_merge_symbols and j < len(symbols):
    merge_symbol_concat, index = get_all_next_consecutive_merge_symbols(symbols[j:], merge_symbols)
    if len(merge_symbol_concat) > 0 and symbols[j + index] not in merge_or_ignore_merge_symbols:
      new_symbol += merge_symbol_concat + symbols[j + index]
      j += index + 1
    else:
      break
  return new_symbol, j


def get_all_next_consecutive_merge_symbols(symbols: Symbols, merge_symbols: Set[Symbol]) -> Tuple[Symbol, int]:
  assert len(symbols) > 0
  merge_symbol_concat = ""
  for index, symbol in enumerate(symbols):
    if symbol in merge_symbols:
      merge_symbol_concat += symbol
    else:
      return merge_symbol_concat, index
  return merge_symbol_concat, index


def merge_left(symbols: Symbols, merge_symbols: Set[Symbol], ignore_merge_symbols: Set[Symbol]) -> Symbols:
  j = 0
  reversed_symbols = symbols[::-1]
  reversed_merged_symbols = []
  while j < len(reversed_symbols):
    new_symbol, j = get_next_merged_symbol_and_index(
      reversed_symbols, j, merge_symbols, ignore_merge_symbols, True)
    reversed_merged_symbols.append(new_symbol)
  merged_symbols = reversed_merged_symbols[::-1]
  return tuple(merged_symbols)


def get_next_merged_symbol_and_index(symbols: Symbols, j: int, merge_symbols: Set[Symbol], ignore_merge_symbols: Set[Symbol], from_left: bool) -> Tuple[Symbol, int]:
  new_symbol = symbols[j]
  j += 1
  if new_symbol not in ignore_merge_symbols and new_symbol not in merge_symbols:
    while j < len(symbols) and symbols[j] in merge_symbols:
      if from_left:
        new_symbol = symbols[j] + new_symbol
      else:
        new_symbol += symbols[j]
      j += 1
  return new_symbol, j

# def add_symbols(symbol_1: Symbol, symbol_2: Symbol, )


def merge_right(symbols: Symbols, merge_symbols: Set[Symbol], ignore_merge_symbols: Set[Symbol]) -> Symbols:
  j = 0
  merged_symbols = []
  while j < len(symbols):
    new_symbol, j = get_next_merged_symbol_and_index(
      symbols, j, merge_symbols, ignore_merge_symbols, False)
    merged_symbols.append(new_symbol)
  return tuple(merged_symbols)


# def is_phonetic_transcription_in_text(text: str) -> bool:
#   # ph_trans_in_text = PH_TRANS_NO_WHITESPACE.match(text)
#   ph_trans_in_text = PH_TRANS.search(text)
#   return ph_trans_in_text is not None


# def is_phonetic_transcription(text: str) -> bool:
#   ipa_of_ph_trans = WHOLE_STRING_IS_PHONETIC_TRANS.search(text)
#   return ipa_of_ph_trans is not None


# @dataclass
# class IPAExtractionSettings():
#   ignore_tones: bool
#   ignore_arcs: bool
#   replace_unknown_ipa_by: str


# def ipa_of_phonetic_transcription(ph_trans: str, logger: Logger) -> str:
#   assert is_phonetic_transcription(ph_trans)
#   resulting_ipa = re.sub(SLASH, '', ph_trans)
#   is_ipa, _ = check_is_ipa_and_return_closest_ipa(resulting_ipa)
#   if not is_ipa:
#     ex = ValueError(f"'{ph_trans}': '{resulting_ipa}' is no valid IPA!")
#     logger.error("", exc_info=ex)
#     raise ex
#   return resulting_ipa


# def check_is_ipa_and_return_closest_ipa(word_ipa: str) -> Tuple[bool, IPAString]:
#   try:
#     ipa = IPAString(unicode_string=word_ipa, ignore=False)
#     return True, ipa
#   except ValueError:
#     ipa = IPAString(unicode_string=word_ipa, ignore=True)
#     return False, ipa


# def extract_from_sentence(ipa_sentence: str, settings: IPAExtractionSettings, merge_stress: bool) -> List[str]:
#   res: List[str] = []
#   tmp: List[str] = []

#   for c in ipa_sentence:
#     if c in string.punctuation or c in string.whitespace:
#       if len(tmp) > 0:
#         raw_word_symbols = _extract_symbols(tmp, settings, merge_stress)
#         res.extend(raw_word_symbols)
#         tmp.clear()
#       res.append(c)
#     else:
#       tmp.append(c)

#   if len(tmp) > 0:
#     raw_word_symbols = _extract_symbols(tmp, settings, merge_stress)
#     res.extend(raw_word_symbols)
#     tmp.clear()
#   return res


# def _extract_symbols(input_symbols: List[str], settings: IPAExtractionSettings, merge_stress: bool) -> List[str]:
#   input_word = ''.join(input_symbols)
#   is_valid_ipa, ipa = check_is_ipa_and_return_closest_ipa(input_word)

#   if not is_valid_ipa:
#     logger = getLogger(__name__)
#     result = [settings.replace_unknown_ipa_by] * len(input_symbols)
#     logger.warning(
#       f"Conversion of '{input_word}' to IPA failed. Result would be: '{ipa}'. Replaced with '{''.join(result)}' instead.")
#     # TODO: Conversion of 'ðӕ' to IPA failed. Result would be: 'ð'. Replaced with '__' instead.
#     return result

#   return ipa_str_to_list(ipa, settings.ignore_tones, settings.ignore_arcs, merge_stress)


# def ipa_str_to_list(ipa_str: IPAString, ignore_tones: bool, ignore_arcs: bool, merge_stress: bool) -> List[str]:
#   symbols: List[str] = []

#   tmp_stress: Optional[str] = None
#   char: IPAChar
#   for char in ipa_str.ipa_chars:
#     char_is_stress = char.unicode_repr in STRESS_SYMBOLS
#     if char_is_stress:
#       if tmp_stress is not None:
#         if merge_stress:
#           tmp_stress = f"{tmp_stress}{char.unicode_repr}"
#         else:
#           symbols.append(tmp_stress)
#           tmp_stress = char.unicode_repr
#       else:
#         tmp_stress = char.unicode_repr
#       continue

#     if char.is_diacritic or char.is_tone:
#       if len(symbols) > 0:
#         if char.is_tone and ignore_tones:
#           continue
#         # I think it is a bug in IPAString that the arc sometimes gets classified as diacritic and sometimes not
#         if char.unicode_repr == ARC:
#           if ignore_arcs:
#             continue
#           # symbols.append(ARC)
#           symbols[-1] += char.unicode_repr
#         else:
#           symbols[-1] += char.unicode_repr
#     else:
#       uc = char.unicode_repr
#       if ignore_arcs:
#         extend_symbols = uc.split(ARC)
#         if tmp_stress is not None:
#           if merge_stress:
#             extend_symbols[0] = f"{tmp_stress}{extend_symbols[0]}"
#           else:
#             extend_symbols = [tmp_stress] + extend_symbols
#           tmp_stress = None
#       else:
#         extend_symbols = [uc]
#         if tmp_stress is not None:
#           if merge_stress:
#             extend_symbols[0] = f"{tmp_stress}{extend_symbols[0]}"
#           else:
#             extend_symbols = [tmp_stress] + extend_symbols
#           tmp_stress = None

#       symbols.extend(extend_symbols)

#   if tmp_stress is not None:
#     symbols.append(tmp_stress)

#   return symbols
