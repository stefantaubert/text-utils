from typing import Dict, List
from typing import OrderedDict as OrderedDictType
from typing import TypeVar

from ordered_set import OrderedSet
from text_utils.text_selection.random_method import (sort_random,
                                                     sort_random_set_cover)
from text_utils.text_selection.utils import get_first_percent
from text_utils.utils import get_until_sum_set, values_to_set

_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")


def get_random_default(data: OrderedDictType[_T1, _T2], seed: int) -> OrderedSet[_T1]:
  result = sort_random(data=data, seed=seed)
  return result


def get_random_cover_default(data: OrderedDictType[_T1, _T2], seed: int) -> OrderedSet[_T1]:
  available_set = values_to_set(data)
  result = sort_random_set_cover(data=available_set, seed=seed)
  return result


def get_random_seconds(data: OrderedDictType[_T1, List[_T2]], seed: int, durations_s: Dict[int, float], seconds: float) -> OrderedSet[_T1]:
  greedy_selected = sort_random(data=data, seed=seed)
  result = get_until_sum_set(greedy_selected, until_values=durations_s, until_value=seconds)
  return result


def get_random_seconds_cover(data: OrderedDictType[_T1, List[_T2]], seed: int, durations_s: Dict[int, float], seconds: float) -> OrderedSet[_T1]:
  available_set = values_to_set(data)
  greedy_selected = sort_random_set_cover(data=available_set, seed=seed)
  result = get_until_sum_set(greedy_selected, until_values=durations_s, until_value=seconds)
  return result


def get_random_count(data: OrderedDictType[_T1, List[_T2]], seed: int, chars: Dict[int, int], count: int) -> OrderedSet[_T1]:
  greedy_selected = sort_random(data=data, seed=seed)
  result = get_until_sum_set(greedy_selected, until_values=chars, until_value=count)
  return result


def get_random_count_cover(data: OrderedDictType[_T1, List[_T2]], seed: int, chars: Dict[int, int], count: int) -> OrderedSet[_T1]:
  available_set = values_to_set(data)
  greedy_selected = sort_random_set_cover(data=available_set, seed=seed)
  result = get_until_sum_set(greedy_selected, until_values=chars, until_value=count)
  return result

def get_random_iterations(data: OrderedDictType[_T1, List[_T2]], seed: int, iterations: int) -> OrderedSet[_T1]:
  greedy_selected = sort_random(data=data, seed=seed)
  result = greedy_selected[:iterations]
  return result


def get_random_iterations_cover(data: OrderedDictType[_T1, List[_T2]], seed: int, iterations: int) -> OrderedSet[_T1]:
  available_set = values_to_set(data)
  greedy_selected = sort_random_set_cover(data=available_set, seed=seed)
  result = greedy_selected[:iterations]
  return result


def get_random_percent(data: OrderedDictType[_T1, List[_T2]], seed: int, percent: float) -> OrderedSet[_T1]:
  greedy_selected = sort_random(data=data, seed=seed)
  result = get_first_percent(greedy_selected, percent)
  return result


def get_random_percent_cover(data: OrderedDictType[_T1, List[_T2]], seed: int, percent: float) -> OrderedSet[_T1]:
  available_set = values_to_set(data)
  greedy_selected = sort_random_set_cover(data=available_set, seed=seed)
  result = get_first_percent(greedy_selected, percent)
  return result
