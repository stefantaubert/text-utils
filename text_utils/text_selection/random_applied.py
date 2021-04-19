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


# def get_n_divergent_random_seconds(data: OrderedDictType[_T1, List[_T2]], seed: int, durations_s: Dict[int, float], seconds: float, n: int) -> List[OrderedSet[_T1]]:
#   available = data
#   backup = None
#   not_available_keys = set()
#   res: List[OrderedSet[_T1]] = []

#   for _ in range(n):
#     tmp = sort_random(data=available, seed=seed)
#     selected, total = get_until_sum_set(tmp, until_values=durations_s, until_value=seconds)

#     if backup is not None:
#       backup_random = sort_random(data=backup, seed=seed)
#       remaining_seconds = seconds - total
#       assert remaining_seconds >= 0
#       result_backup, total = get_until_sum_set(
#         backup_random, until_values=durations_s, until_value=remaining_seconds)
#       selected |= result_backup

#     res.append(selected)

#     not_available_keys |= selected
#     available_keys = set(data.keys()).difference(not_available_keys)
#     all_were_selected = len(available_keys) == 0

#     if all_were_selected:
#       not_available_keys = set()
#       available = data
#       backup = None
#     else:
#       available = OrderedDict({k: v for k, v in data.items() if k in available_keys})
#       backup = OrderedDict({k: v for k, v in data.items() if k in not_available_keys})
#   return res

def get_n_divergent_random_seconds(data: OrderedDictType[_T1, List[_T2]], seed: int, durations_s: Dict[int, float], seconds: float, n: int = 3) -> List[OrderedSet[_T1]]:
  data_keys = list(data.keys())
  random.seed(seed)
  random.shuffle(data_keys)
  total_dur = np.sum(list(durations_s.values()))
  dur_to_fill = n * seconds
  stack_times = math.ceil(dur_to_fill / total_dur)
  data_keys *= stack_times
  step_length = int(np.round(total_dur / n))
  res: List[OrderedSet[_T1]] = []

  for index in range(n):
    selected, _ = get_until_sum_set(
      data_keys[index * step_length:], until_values=durations_s, until_value=seconds)
    res.append(selected)
  return res


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
