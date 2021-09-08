import re
from typing import Dict, Optional, Set

from text_utils.types import Symbol, Symbols

ARPABET_IPA_MAP: Dict[Symbol, Symbol] = {
  # "A": "ə",
  "AA": "ɑ",
  "AE": "æ",
  "AH": "ʌ",  # ə
  "AO": "ɔ",
  "AW": "aʊ",
  "AY": "aɪ",
  "B": "b",
  "CH": "ʧ",
  "D": "d",  # ð
  "DH": "ð",
  "EH": "ɛ",
  "ER": "ɝ",  # ər
  "EY": "eɪ",
  "F": "f",
  "G": "g",
  "HH": "h",
  "IH": "ɪ",
  "IY": "i",
  "JH": "ʤ",  # alt: d͡ʒ
  "K": "k",
  "L": "l",
  "M": "m",
  "N": "n",
  "NG": "ŋ",
  "OW": "oʊ",
  "OY": "ɔɪ",
  "P": "p",
  "R": "ɹ",
  "S": "s",
  "SH": "ʃ",
  "T": "t",
  "TH": "θ",
  "UH": "ʊ",
  "UW": "u",
  "V": "v",
  "W": "w",
  "Y": "j",
  "Z": "z",
  "ZH": "ʒ",
}

IPA_STRESSES: Dict[str, Symbol] = {
  "0": "",
  "1": "ˈ",
  "2": "ˌ",
}

ALL_ARPABET_SYMBOLS_WITH_STRESS: Set[Symbol] = {
  k + s for k in ARPABET_IPA_MAP for s in IPA_STRESSES.keys() | {""}
}

ARPABET_PATTERN: str = re.compile(r"([A-Z]+)(\d*)")


def get_ipa_mapping_with_stress(arpa_symbol: Symbol) -> Symbol:
  res = re.match(ARPABET_PATTERN, arpa_symbol)
  assert res is not None
  phon, stress = res.groups()
  ipa_phoneme = ARPABET_IPA_MAP[phon]
  has_stress = stress != ''

  if has_stress:
    ipa_stress = IPA_STRESSES[stress]
    ipa_phoneme = f"{ipa_stress}{ipa_phoneme}"

  return ipa_phoneme


def has_ipa_mapping(arpa_symbol: Symbol) -> bool:
  return arpa_symbol in ALL_ARPABET_SYMBOLS_WITH_STRESS
  # res = re.match(ARPABET_PATTERN, arpa_symbol)
  # return res is not None


def symbols_map_arpa_to_ipa(arpa_symbols: Symbols, ignore: Set[Symbol], replace_unknown: bool, replace_unknown_with: Optional[Symbol]) -> Symbols:
  ipa_symbols = []
  for arpa_symbol in arpa_symbols:
    new_symbol = symbol_map_arpa_to_ipa(
      arpa_symbol=arpa_symbol,
      ignore=ignore,
      replace_unknown=replace_unknown,
      replace_unknown_with=replace_unknown_with,
    )
    if new_symbol is not None:
      ipa_symbols.append(new_symbol)
  return tuple(ipa_symbols)


def symbol_map_arpa_to_ipa(arpa_symbol: Symbol, ignore: Set[Symbol], replace_unknown: bool, replace_unknown_with: Optional[Symbol]) -> Optional[Symbol]:
  assert isinstance(arpa_symbol, str)
  if arpa_symbol in ignore:
    return arpa_symbol
  if has_ipa_mapping(arpa_symbol):
    return get_ipa_mapping_with_stress(arpa_symbol)
  if replace_unknown:
    if replace_unknown_with is None or replace_unknown_with == "":
      return None
    return replace_unknown_with
  return arpa_symbol
