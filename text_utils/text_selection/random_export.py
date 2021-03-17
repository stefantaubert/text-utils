from typing import Any, Dict, List, Optional
from typing import OrderedDict as OrderedDictType
from typing import Set

from ordered_set import OrderedSet
from text_utils.text_selection.random_applied import (
    get_random_count, get_random_count_cover, get_random_cover_default,
    get_random_default, get_random_iterations, get_random_iterations_cover,
    get_random_seconds, get_random_seconds_cover)
from text_utils.text_selection.utils import get_filtered_ngrams


def random_default(data: OrderedDictType[int, Any], seed: int) -> OrderedSet[int]:
  return get_random_default(
    data=data,
    seed=seed,
  )


def random_seconds(data: OrderedDictType[int, Any], seed: int, durations_s: Dict[int, float], seconds: float) -> OrderedSet[int]:
  return get_random_seconds(
    data=data,
    seed=seed,
    durations_s=durations_s,
    seconds=seconds,
  )


def random_count(data: OrderedDictType[int, Any], seed: int, chars: Dict[int, int], count: int) -> OrderedSet[int]:
  return get_random_count(
    data=data,
    seed=seed,
    chars=chars,
    count=count,
  )


def random_iterations(data: OrderedDictType[int, Any], seed: int, iterations: int) -> OrderedSet[int]:
  return get_random_iterations(
    data=data,
    seed=seed,
    iterations=iterations,
  )


def random_ngrams_default_cover(data: OrderedDictType[int, List[str]], n_gram: int, ignore_symbols: Optional[Set[str]], seed: int) -> OrderedSet[int]:
  data_ngrams = get_filtered_ngrams(data, n_gram, ignore_symbols)
  return get_random_cover_default(
    data=data_ngrams,
    seed=seed,
  )


def random_ngrams_seconds_cover(data: OrderedDictType[int, List[str]], n_gram: int, ignore_symbols: Optional[Set[str]], seed: int, durations_s: Dict[int, float], seconds: float) -> OrderedSet[int]:
  data_ngrams = get_filtered_ngrams(data, n_gram, ignore_symbols)
  return get_random_seconds_cover(
    data=data_ngrams,
    seed=seed,
    durations_s=durations_s,
    seconds=seconds,
  )


def random_ngrams_iterations_cover(data: OrderedDictType[int, List[str]], n_gram: int, ignore_symbols: Optional[Set[str]], seed: int, iterations: int) -> OrderedSet[int]:
  data_ngrams = get_filtered_ngrams(data, n_gram, ignore_symbols)
  return get_random_iterations_cover(
    data=data_ngrams,
    seed=seed,
    iterations=iterations,
  )


def random_ngrams_count_cover(data: OrderedDictType[int, List[str]], n_gram: int, ignore_symbols: Optional[Set[str]], seed: int, chars: Dict[int, int], count: int) -> OrderedSet[int]:
  data_ngrams = get_filtered_ngrams(data, n_gram, ignore_symbols)
  return get_random_count_cover(
    data=data_ngrams,
    seed=seed,
    chars=chars,
    count=count,
  )
