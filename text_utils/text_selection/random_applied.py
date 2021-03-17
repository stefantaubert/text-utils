from typing import Dict, List, Tuple, TypeVar

from text_utils.text_selection.random_method import (sort_random,
                                                     sort_random_set_cover)
from text_utils.utils import (get_first_n, get_until_sum,
                              select_enties_from_ordereddict, values_to_set)

_T = TypeVar("_T")


def random_seconds(available: Dict[int, List[_T]], seed: int, durations_s: Dict[int, float], seconds: float) -> Dict[int, List[_T]]:
  greedy_selected = sort_random(ngrams=available, seed=seed)
  part = get_until_sum(greedy_selected, until_values=durations_s, until_value=seconds)
  result = select_enties_from_ordereddict(available, set(part.keys()))
  return result


def random_seconds_cover(available: Dict[int, List[_T]], seed: int, durations_s: Dict[int, float], seconds: float) -> Dict[int, List[_T]]:
  available_set = values_to_set(available)
  greedy_selected = sort_random_set_cover(ngrams=available_set, seed=seed)
  part = get_until_sum(greedy_selected, until_values=durations_s, until_value=seconds)
  result = select_enties_from_ordereddict(available, set(part.keys()))
  return result


def random_count(available: Dict[int, List[_T]], seed: int, chars: Dict[int, int], count: int) -> Dict[int, List[_T]]:
  greedy_selected = sort_random(ngrams=available, seed=seed)
  part = get_until_sum(greedy_selected, until_values=chars, until_value=count)
  result = select_enties_from_ordereddict(available, set(part.keys()))
  return result


def random_count_cover(available: Dict[int, List[_T]], seed: int, chars: Dict[int, int], count: int) -> Dict[int, List[_T]]:
  available_set = values_to_set(available)
  greedy_selected = sort_random_set_cover(ngrams=available_set, seed=seed)
  part = get_until_sum(greedy_selected, until_values=chars, until_value=count)
  result = select_enties_from_ordereddict(available, set(part.keys()))
  return result


def random_iterations(available: Dict[int, List[_T]], seed: int, iterations: int) -> Dict[int, List[_T]]:
  greedy_selected = sort_random(ngrams=available, seed=seed)
  part = get_first_n(greedy_selected, n=iterations)
  result = select_enties_from_ordereddict(available, set(part.keys()))
  return result


def random_iterations_cover(available: Dict[int, List[_T]], seed: int, iterations: int) -> Dict[int, List[_T]]:
  available_set = values_to_set(available)
  greedy_selected = sort_random_set_cover(ngrams=available_set, seed=seed)
  part = get_first_n(greedy_selected, n=iterations)
  result = select_enties_from_ordereddict(available, set(part.keys()))
  return result
