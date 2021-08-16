from logging import Logger
from typing import List, Optional, Tuple

from text_utils.ipa2symb import IPAExtractionSettings
from text_utils.language import Language
from text_utils.symbol_id_dict import SymbolIdDict
from text_utils.text import (EngToIpaMode, text_normalize, text_to_ipa,
                             text_to_symbols)


def symbols_normalize(symbols: List[str], lang: Language, accent_ids: List[str], logger: Logger) -> Tuple[List[str], List[int]]:
  assert len(symbols) == len(accent_ids)
  orig_text = SymbolIdDict.symbols_to_text(symbols)
  text = text_normalize(
    text=orig_text,
    lang=lang,
    logger=logger,
  )

  if lang != Language.IPA:
    new_symbols: List[str] = text_to_symbols(
      text=text,
      lang=lang,
      ipa_settings=None,
      logger=logger,
      merge_stress=None,
    )
    if len(accent_ids) > 0:
      new_accent_ids = [accent_ids[0]] * len(new_symbols)
    else:
      new_accent_ids = []
  else:
    # normalization of ipa not supported, maybe support remove whitespace and update accents
    new_symbols = symbols
    new_accent_ids = accent_ids
  assert len(new_symbols) == len(new_accent_ids)
  return new_symbols, new_accent_ids


def symbols_to_ipa(symbols: List[str], lang: Language, accent_ids: List[str], ignore_tones: bool, ignore_arcs: bool, mode: Optional[EngToIpaMode], replace_unknown_with: Optional[str], consider_ipa_annotations: bool, logger: Logger, merge_stress: Optional[bool] = True) -> Tuple[List[str], List[int]]:
  assert len(symbols) == len(accent_ids)
  # TODO: also for ipa symbols to have possibility to remove arcs and tones
  orig_text = SymbolIdDict.symbols_to_text(symbols)
  ipa = text_to_ipa(
    text=orig_text,
    lang=lang,
    mode=mode,
    logger=logger,
    replace_unknown_with=replace_unknown_with,
    consider_ipa_annotations=consider_ipa_annotations,
  )

  settings = IPAExtractionSettings(
    ignore_arcs=ignore_arcs,
    ignore_tones=ignore_tones,
    replace_unknown_ipa_by=replace_unknown_with,
  )

  new_symbols: List[str] = text_to_symbols(
    text=ipa,
    lang=Language.IPA,
    ipa_settings=settings,
    logger=logger,
    merge_stress=merge_stress,
  )

  if len(accent_ids) > 0:
    new_accent_ids = [accent_ids[0]] * len(new_symbols)
  else:
    new_accent_ids = []
  assert len(new_symbols) == len(new_accent_ids)
  return new_symbols, new_accent_ids
