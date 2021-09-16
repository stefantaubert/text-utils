from typing import Dict, Optional, Set

from text_utils.pronunciation.arpa_symbols import (AA, AE, AH, AO, AW, AX, AXR,
                                                   AY, CH)
from text_utils.pronunciation.arpa_symbols import CONSONANTS as ARPA_CONSONANTS
from text_utils.pronunciation.arpa_symbols import (DH, DX, EH, EL, EM, EN, ER,
                                                   EY, HH, IH, IX, IY, JH, NG,
                                                   NX, OW, OY, SH)
from text_utils.pronunciation.arpa_symbols import \
    STRESS_NONE as ARPA_STRESS_NONE
from text_utils.pronunciation.arpa_symbols import \
    STRESS_NONE_ALT as ARPA_STRESS_NONE_ALT
from text_utils.pronunciation.arpa_symbols import \
    STRESS_PRIMARY as ARPA_STRESS_PRIMARY
from text_utils.pronunciation.arpa_symbols import \
    STRESS_SECONDARY as ARPA_STRESS_SECONDARY
from text_utils.pronunciation.arpa_symbols import TH, UH, UW, UX
from text_utils.pronunciation.arpa_symbols import VOWELS as ARPA_VOWELS
from text_utils.pronunciation.arpa_symbols import (WH, ZH, B, D, F, G, H, K, L,
                                                   M, N, P, Q, R, S, T, V, W,
                                                   Y, Z)
from text_utils.pronunciation.ipa_symbols import \
    STRESS_PRIMARY as IPA_STRESS_PRIMARY
from text_utils.pronunciation.ipa_symbols import \
    STRESS_SECONDARY as IPA_STRESS_SECONDARY
from text_utils.types import Symbol, Symbols

__ARPABET_IPA_MAP_STRESSLESS: Dict[Symbol, Symbol] = {
    AA: "ɑ",
    AE: "æ",
    AH: "ʌ",
    AO: "ɔ",
    AW: "aʊ",
    AX: "ə",
    AXR: "ɚ",
    AY: "aɪ",
    EH: "ɛ",
    ER: "ɝ",
    EY: "eɪ",
    IH: "ɪ",
    IX: "ɨ",
    IY: "i",
    OW: "oʊ",
    OY: "ɔɪ",
    UH: "ʊ",
    UW: "u",
    UX: "ʉ",
    B: "b",
    CH: "t͡ʃ",
    D: "d",
    DH: "ð",
    DX: "ɾ",
    EL: "l̩",
    EM: "m̩",
    EN: "n̩",
    F: "f",
    G: "ɡ",
    HH: "h",
    H: "h",
    JH: "d͡ʒ",
    K: "k",
    L: "l",
    M: "m",
    N: "n",
    NG: "ŋ",
    NX: "ɾ̃",
    P: "p",
    Q: "ʔ",
    R: "ɹ",
    S: "s",
    SH: "ʃ",
    T: "t",
    TH: "θ",
    V: "v",
    W: "w",
    WH: "ʍ",
    Y: "j",
    Z: "z",
    ZH: "ʒ",
}

__IPA_TO_ARPA_STRESSES: Dict[Symbol, Symbol] = {
  ARPA_STRESS_NONE_ALT: "",
  ARPA_STRESS_NONE: "",
  ARPA_STRESS_PRIMARY: IPA_STRESS_PRIMARY,
  ARPA_STRESS_SECONDARY: IPA_STRESS_SECONDARY,
}

__ARPABET_VOWEL_IPA_MAP: Dict[Symbol, Symbol] = {
  f"{arpa_symbol}{arpa_stress}": f"{__IPA_TO_ARPA_STRESSES[arpa_stress]}{__ARPABET_IPA_MAP_STRESSLESS[arpa_symbol]}" for arpa_symbol in ARPA_VOWELS for arpa_stress in __IPA_TO_ARPA_STRESSES
}

__ARPABET_CONSONANT_IPA_MAP: Dict[Symbol, Symbol] = {
  consonant: __ARPABET_IPA_MAP_STRESSLESS[consonant] for consonant in ARPA_CONSONANTS}

__ARPABET_IPA_MAP = dict(**__ARPABET_VOWEL_IPA_MAP, **__ARPABET_CONSONANT_IPA_MAP)


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
  has_ipa_mapping = arpa_symbol in __ARPABET_IPA_MAP
  if has_ipa_mapping:
    return __ARPABET_IPA_MAP[arpa_symbol]
  if replace_unknown:
    if replace_unknown_with is None or replace_unknown_with == "":
      return None
    return replace_unknown_with
  return arpa_symbol
