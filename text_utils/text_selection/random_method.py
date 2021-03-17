import random
from collections import OrderedDict
from typing import Dict, Optional
from typing import OrderedDict as OrderedDictType
from typing import Set, TypeVar, Union

_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")


def sort_random(ngrams: Dict[_T1, _T2], seed: int) -> OrderedDictType[_T1, _T2]:
  random.seed(seed)
  result: OrderedDictType[_T1, _T2] = OrderedDict()
  all_keys = list(ngrams.keys())
  random.shuffle(all_keys)
  result = OrderedDict({key: ngrams[key] for key in all_keys})
  return result


def sort_random_set_cover(ngrams: Dict[_T1, Set[_T2]], seed: int):
  """first select randomly to cover all occuring ngrams, then normal random"""
  all_ngrams = {x for y in ngrams.values() for x in y}
  result: OrderedDictType[_T1, _T2] = OrderedDict()
  random.seed(seed)
  covered = set()
  available = ngrams.copy()
  while covered != all_ngrams:
    not_covered = all_ngrams - covered
    possible = {k: v for k, v in available.items() if len(not_covered.intersection(v)) > 0}
    possible_keys = list(possible.keys())
    choosen_key = random.choice(possible_keys)
    result[choosen_key] = available[choosen_key]
    covered |= available[choosen_key]
    available.pop(choosen_key)
  all_remaining_keys = list(available.keys())
  random.shuffle(all_remaining_keys)
  for k in all_remaining_keys:
    result[k] = available[k]
  return result
