from logging import getLogger
from typing import Dict, List, Optional
from typing import OrderedDict as OrderedDictType
from typing import Set

from ordered_set import OrderedSet
from text_utils.text_selection.greedy_applied import (greedy_default, greedy_count,
                                                      greedy_epochs,
                                                      greedy_iterations,
                                                      greedy_seconds)
from text_utils.text_selection.utils import get_filtered_ngrams


def greedy_ngrams_default(data: OrderedDictType[int, List[str]], n_gram: int, ignore_symbols: Optional[Set[str]]) -> OrderedSet[int]:
  return greedy_default(
    data=get_filtered_ngrams(data, n_gram, ignore_symbols),
  )


def greedy_ngrams_seconds(data: OrderedDictType[int, List[str]], n_gram: int, ignore_symbols: Optional[Set[str]], durations_s: Dict[int, float], seconds: float) -> OrderedSet[int]:
  return greedy_seconds(
    data=get_filtered_ngrams(data, n_gram, ignore_symbols),
    durations_s=durations_s,
    seconds=seconds,
  )


def greedy_ngrams_count(data: OrderedDictType[int, List[str]], n_gram: int, ignore_symbols: Optional[Set[str]], chars: Dict[int, int], total_count: int) -> OrderedSet[int]:
  return greedy_count(
    data=get_filtered_ngrams(data, n_gram, ignore_symbols),
    chars=chars,
    total_count=total_count,
  )


def greedy_ngrams_iterations(data: OrderedDictType[int, List[str]], n_gram: int, ignore_symbols: Optional[Set[str]], iterations: int) -> OrderedSet[int]:
  return greedy_iterations(
    data=get_filtered_ngrams(data, n_gram, ignore_symbols),
    iterations=iterations,
  )


def greedy_ngrams_epochs(data: OrderedDictType[int, List[str]], n_gram: int, ignore_symbols: Optional[Set[str]], epochs: int) -> OrderedSet[int]:
  return greedy_epochs(
    data=get_filtered_ngrams(data, n_gram, ignore_symbols),
    epochs=epochs,
  )
