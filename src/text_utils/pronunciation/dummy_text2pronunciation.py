from typing import Dict, Optional, Set, Tuple, Union

from sentence2pronunciation import sentence2pronunciation
from text_utils.types import Symbols


def get_sentence2pronunciaton(sentence: str, dictionary: Dict[str, Tuple[str, ...]], trim_symb: Set[str], split_on_hyphen: bool, replace_unknown_with: Union[str, Tuple[str, ...]], consider_annotations: bool, annotation_indicator: Optional[str] = "/", use_cache: bool = True, ignore_case_in_cache: Optional[bool] = True) -> Symbols:
  words = sentence.split()
  result = []
  for word in words:
    word = word.upper()
    if word in dictionary:
      result.extend(list(dictionary[word]))
    else:
      result.extend(list(replace_unknown_with(word)))
    result.append(" ")

  return tuple(result)


def get_sentence2pronunciaton2(sentence: str, trim_symb: Set[str], split_on_hyphen: bool, lookup: Union[str, Tuple[str, ...]], consider_annotations: bool, annotation_indicator: Optional[str] = "/", use_cache: bool = True, ignore_case_in_cache: Optional[bool] = True) -> Symbols:
  words = sentence.split()
  result = []
  for word in words:
    pron = lookup(word)
    result.extend(list(pron))
    result.append(" ")

  return tuple(result)
