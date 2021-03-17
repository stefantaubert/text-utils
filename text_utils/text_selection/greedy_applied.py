from typing import Dict, List
from typing import OrderedDict as OrderedDictType
from typing import Tuple, TypeVar

from ordered_set import OrderedSet
from text_utils.text_selection.greedy_methods import (sort_greedy,
                                                      sort_greedy_epochs,
                                                      sort_greedy_until)
from text_utils.utils import values_to_set

_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")


def greedy_seconds(data: OrderedDictType[_T1, List[_T2]], durations_s: Dict[int, float], seconds: float) -> OrderedSet[_T1]:
  available_set = values_to_set(data)
  result = sort_greedy_until(
    ngrams=available_set, until_values=durations_s, until_value=seconds)
  return result


def greedy_count(data: OrderedDictType[_T1, List[_T2]], chars: Dict[int, int], total_count: int) -> OrderedSet[_T1]:
  available_set = values_to_set(data)
  result = sort_greedy_until(
    ngrams=available_set, until_values=chars, until_value=total_count)
  return result


def greedy_epochs(data: OrderedDictType[_T1, List[_T2]], epochs: int) -> OrderedSet[_T1]:
  available_set = values_to_set(data)
  result = sort_greedy_epochs(ngrams=available_set, epochs=epochs)
  return result


def greedy_iterations(data: OrderedDictType[_T1, List[_T2]], iterations: int) -> OrderedSet[_T1]:
  # maybe own method in greedy_methods
  greedy_selected = greedy_default(data)
  result = greedy_selected[:iterations]
  return result


def greedy_default(data: OrderedDictType[_T1, List[_T2]]) -> OrderedSet[_T1]:
  # maybe own method in greedy_methods
  available_set = values_to_set(data)
  result = sort_greedy(ngrams=available_set)
  return result
