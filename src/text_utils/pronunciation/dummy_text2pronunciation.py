from functools import partial
from typing import Callable, Dict, Optional, Set

from sentence2pronunciation import \
    sentence2pronunciaton as sentence2pronunciaton_orig
from sentence2pronunciation.core import Pronunciation, Symbol


def lookup_dict(word: str, dictionary: Dict[Pronunciation, Pronunciation], replace_unknown_with: Callable[[Pronunciation], Pronunciation]) -> Pronunciation:
  word_upper = word.upper()
  if word_upper in dictionary:
    return dictionary[word_upper][0]
  return replace_unknown_with(word)


def sentence2pronunciaton(sentence: Pronunciation, dictionary: Dict[Pronunciation, Pronunciation], trim_symbols: Set[Symbol], split_on_hyphen: bool, replace_unknown_with: Callable[[Pronunciation], Pronunciation], consider_annotation: bool, annotation_split_symbol: Optional[Symbol], use_cache: bool, ignore_case_in_cache: Optional[bool]) -> Pronunciation:
  assert isinstance(sentence, tuple)
  method = partial(lookup_dict, dictionary=dictionary, replace_unknown_with=replace_unknown_with)
  result = sentence2pronunciaton_orig(
    sentence=''.join(sentence),
    annotation_split_symbol=annotation_split_symbol,
    consider_annotation=consider_annotation,
    get_pronunciation=method,
    split_on_hyphen=split_on_hyphen,
    trim_symbols=trim_symbols,
  )
  return result


def sentence2pronunciaton2(sentence: Pronunciation, trim_symb: Set[Symbol], split_on_hyphen: bool, lookup: Callable[[Pronunciation], Pronunciation], consider_annotations: bool, annotation_indicator: Optional[str], use_cache: bool, ignore_case_in_cache: Optional[bool]) -> Pronunciation:
  assert isinstance(sentence, tuple)
  result = sentence2pronunciaton_orig(
    sentence=''.join(sentence),
    annotation_split_symbol=annotation_indicator,
    consider_annotation=consider_annotations,
    get_pronunciation=lookup,
    split_on_hyphen=split_on_hyphen,
    trim_symbols=trim_symb,
  )
  return result
