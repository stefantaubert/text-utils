import math
import random
from collections import OrderedDict
from typing import Dict, List, Optional
from typing import OrderedDict as OrderedDictType
from typing import Set, Tuple, TypeVar

import numpy as np
from ordered_set import OrderedSet
from text_utils.text_selection.random_method import (sort_random,
                                                     sort_random_set_cover)
from text_utils.text_selection.utils import find_unlike_sets, get_first_percent
from text_utils.utils import get_until_sum_set, values_to_set
from tqdm import tqdm

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
  result, _ = get_until_sum_set(greedy_selected, until_values=durations_s, until_value=seconds)
  return result


def get_n_divergent_random_seconds(durations_s: OrderedDictType[int, float], seconds: float, n: int = 3) -> List[OrderedSet[_T1]]:
  data_keys = list(durations_s.keys())
  # random.seed(seed)
  # random.shuffle(data_keys)
  total_dur = sum(durations_s.values())
  dur_to_fill = n * seconds
  stack_times = math.ceil(dur_to_fill / total_dur)
  data_keys *= stack_times
  step_length = round(total_dur / n)

  selected, _ = get_until_sum_set(
      data_keys, until_values=durations_s, until_value=seconds)
  selected = list(selected)
  res: List[OrderedSet[_T1]] = [selected]

  for _ in range(n - 1):
    start_index = get_right_start_index(step_length, durations_s, res[-1], data_keys)
    selected, _ = get_until_sum_set(
      data_keys[start_index:], until_values=durations_s, until_value=seconds)
    selected = list(selected)
    res.append(selected)
  return res


def get_right_start_index(step_length: int, durations_s: OrderedDictType[int, float], prev_vec: List[_T1], data_keys: List[int]) -> int:
  # der Startindex soll auf das Element in data_keys referieren, das zu dem ersten Element in prev_vec mindestens den Abstand step_length hat (d.h. genau diesen Abstand hat oder das erste Element ist, für das dieser Abstand überschritten wird). Abstand haben bedeutet hier die aufsummierten Durations
  """
  Bsp: step_length = 4
       durations = {0: 1, 1: 2, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2}
       prev_vec = [0,1,2,3]
       Es ist das Element in {0,...,6} gesucht, das zu 0 mindestens Abstand 4 hat
       Das wäre hier die 2, denn Entfernung(0,2) = dur(1) + dur(2) = 2+3>4
  """
  dur_sum = 0
  index = 0
  while dur_sum < step_length:
    index += 1
    if index == len(prev_vec):
      prev_element = prev_vec[-1]
      start_index = data_keys.index(prev_element) + 1
      return start_index
    dur_sum += durations_s[prev_vec[index]]
  # if index < len(prev_vec):
  start_element = prev_vec[index]
  start_index = data_keys.index(start_element)
  return start_index


# def get_right_start_index(step_length: int, durations_s: OrderedDictType[int, float], prev_vec: List[_T1], data_keys: List[int]) -> int:
#   dur_sum = 0
#   backwards_index = -1
#   while dur_sum < step_length:
#     dur_sum += durations_s[prev_vec[backwards_index]]
#     backwards_index -= 1
#   start_element = prev_vec[backwards_index]
#   start_index = data_keys.index(start_element)
#   return start_index


def get_random_seconds_divergence_seeds(data: OrderedDictType[_T1, List[_T2]], seed: int, durations_s: Dict[int, float], seconds: float, samples: int, n: int) -> Tuple[OrderedSet[int], List[OrderedSet[_T1]]]:
  potential_seeds = range(samples)
  # random.shuffle(potential_seeds)

  potential_sets: List[OrderedSet[_T1]] = []
  for sample_seed in tqdm(potential_seeds):
    sample_set = get_random_seconds(
      data=data,
      seed=sample_seed,
      durations_s=durations_s,
      seconds=seconds,
    )
    potential_sets.append(sample_set)

  selected_set_idxs = sorted(find_unlike_sets(potential_sets, n, seed))
  selected_seeds = OrderedSet({potential_seeds[i] for i in selected_set_idxs})
  selected_sets = [potential_sets[i] for i in selected_set_idxs]
  return selected_seeds, selected_sets


def get_random_seconds_cover(data: OrderedDictType[_T1, List[_T2]], seed: int, durations_s: Dict[int, float], seconds: float) -> OrderedSet[_T1]:
  available_set = values_to_set(data)
  greedy_selected = sort_random_set_cover(data=available_set, seed=seed)
  result, _ = get_until_sum_set(greedy_selected, until_values=durations_s, until_value=seconds)
  return result


def get_random_count(data: OrderedDictType[_T1, List[_T2]], seed: int, chars: Dict[int, int], count: int) -> OrderedSet[_T1]:
  greedy_selected = sort_random(data=data, seed=seed)
  result, _ = get_until_sum_set(greedy_selected, until_values=chars, until_value=count)
  return result


def get_random_count_cover(data: OrderedDictType[_T1, List[_T2]], seed: int, chars: Dict[int, int], count: int) -> OrderedSet[_T1]:
  available_set = values_to_set(data)
  greedy_selected = sort_random_set_cover(data=available_set, seed=seed)
  result, _ = get_until_sum_set(greedy_selected, until_values=chars, until_value=count)
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
