import re
from typing import Dict, Optional, Set, Tuple

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

ARPABET_PATTERN: str = re.compile(r"([A-Z]+)(\d*)")


def get_ipa_mapping_with_stress(arpa_symbol: Symbol, include_stress: bool) -> Symbol:
  res = re.match(ARPABET_PATTERN, arpa_symbol)
  assert res is not None
  phon, stress = res.groups()
  ipa_phoneme = ARPABET_IPA_MAP[phon]
  has_stress = stress != ''

  if has_stress and include_stress:
    ipa_stress = IPA_STRESSES[stress]
    ipa_phoneme = f"{ipa_stress}{ipa_phoneme}"

  return ipa_phoneme


def has_ipa_mapping(arpa_symbol: Symbol) -> bool:
  res = re.match(ARPABET_PATTERN, arpa_symbol)
  return res is not None


def map_arpa_to_ipa(arpa_symbols: Symbols, ignore: Set[Symbol], replace_unknown: bool, replace_unknown_with: Optional[Symbol], include_stress: bool) -> Symbols:
  ipa_symbols = []
  for arpa_symbol in arpa_symbols:
    assert isinstance(arpa_symbol, str)
    if has_ipa_mapping(arpa_symbol):
      ipa_symbols.append(get_ipa_mapping_with_stress(arpa_symbol, include_stress))
    elif arpa_symbol in ignore:
      ipa_symbols.append(arpa_symbol)
    elif replace_unknown:
      if replace_unknown_with is None or replace_unknown_with == "":
        continue
      ipa_symbols.append(replace_unknown_with)
    else:
      ipa_symbols.append(arpa_symbol)
  result = tuple(ipa_symbols)
  return result
