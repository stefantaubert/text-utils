from functools import partial
from typing import Callable, Dict, Optional, Set, Tuple

from sentence2pronunciation import sentence2pronunciaton
from text_utils.types import Symbols


def lookup_dict(word: str, dictionary: Dict[str, Tuple[str, ...]], replace_unknown_with: Callable[[str], Tuple[str, ...]]) -> Tuple[str, ...]:
  word_upper = word.upper()
  if word_upper in dictionary:
    return dictionary[word_upper][0]
  return replace_unknown_with(word)


def get_sentence2pronunciaton(sentence: str, dictionary: Dict[str, Tuple[str, ...]], trim_symb: Set[str], split_on_hyphen: bool, replace_unknown_with: Callable[[str], Tuple[str, ...]], consider_annotations: bool, annotation_indicator: Optional[str] = "/", use_cache: bool = True, ignore_case_in_cache: Optional[bool] = True) -> Symbols:
  method = partial(lookup_dict, dictionary=dictionary, replace_unknown_with=replace_unknown_with)
  result = sentence2pronunciaton(
    sentence=sentence,
    annotation_split_symbol=annotation_indicator,
    cons_annotation=consider_annotations,
    get_pronun=method,
    split_on_hyphen=split_on_hyphen,
    trim_symb=trim_symb,
  )
  return result


def get_sentence2pronunciaton2(sentence: str, trim_symb: Set[str], split_on_hyphen: bool, lookup: Callable[[str], Tuple[str, ...]], consider_annotations: bool, annotation_indicator: Optional[str] = "/", use_cache: bool = True, ignore_case_in_cache: Optional[bool] = True) -> Symbols:
  result = sentence2pronunciaton(
    sentence=sentence,
    annotation_split_symbol=annotation_indicator,
    cons_annotation=consider_annotations,
    get_pronun=lookup,
    split_on_hyphen=split_on_hyphen,
    trim_symb=trim_symb,
  )
  return result
