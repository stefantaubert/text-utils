from collections import Counter, OrderedDict
from logging import getLogger
from typing import Dict, List, Optional
from typing import OrderedDict as OrderedDictType
from typing import Set, Tuple, TypeVar

from ordered_set import OrderedSet
from text_utils.text import get_ngrams
from text_utils.utils import filter_ngrams

_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")


def get_top_n(data: OrderedDictType[int, List[_T1]], top_percent: float) -> OrderedSet[_T1]:
  """
  if the distribution is same then it will take the _T1 by ascending sorting to make it deterministic
  """
  distr = get_distribution(data)
  top_n = round(len(distr) * top_percent)
  distr_sorted_after_key = OrderedDict(sorted(distr.items(), key=lambda x: x[0], reverse=False))
  distr_sorted = OrderedDict(sorted(distr_sorted_after_key.items(),
                             key=lambda x: x[1], reverse=True))
  top_ngrams: OrderedSet[_T1] = OrderedSet(list(distr_sorted.keys())[:top_n])
  return top_ngrams


def get_distribution(ngrams: Dict[_T1, List[_T2]]) -> Dict[_T2, float]:
  ngrams_counter = Counter(x for y in ngrams.values() for x in y)
  vals = list(ngrams_counter.values())
  sum_vals = sum(vals)
  distr: Dict[_T2, float] = {k: v / sum_vals for k, v in ngrams_counter.items()}
  return distr


def get_reverse_distribution(ngrams: Dict[_T1, List[_T2]]) -> Dict[_T2, float]:
  ngrams_counter = Counter(x for y in ngrams.values() for x in y)
  keys_sorted = list(sorted(ngrams_counter.keys()))
  od = OrderedDict({k: ngrams_counter[k] for k in keys_sorted})
  vals = list(od.values())
  sum_vals = sum(vals)
  distr: Dict[_T2, float] = {k: vals[i] / sum_vals for i, k in enumerate(reversed(keys_sorted))}
  return distr


def get_filtered_ngrams(data: OrderedDictType[int, List[str]], n_gram: int, ignore_symbols: Optional[Set[str]]) -> OrderedDictType[int, List[Tuple]]:
  assert isinstance(data, OrderedDict)

  logger = getLogger(__name__)
  logger.info(f"Calculating {n_gram}-grams...")
  available_ngrams: OrderedDictType[int, List[Tuple]] = OrderedDict({
    k: get_ngrams(v, n_gram) for k, v in data.items()
  })

  occurring_symbols = {x for y in data.values() for x in y}
  occurring_symbols_count = len(occurring_symbols)
  occurring_ngrams = {x for y in available_ngrams.values() for x in y}
  occurring_ngrams_count = len(occurring_ngrams)

  logger.info(
      f"Theoretically, the maximum amount of unique {n_gram}-grams is: {occurring_symbols_count ** n_gram}.")

  if occurring_symbols_count > 0:
    logger.info(
      f"The amount of unique occurring {n_gram}-grams is: {occurring_ngrams_count} ({occurring_ngrams_count/(occurring_symbols_count ** n_gram)*100:.2f}%).")

  if ignore_symbols is not None:
    occuring_ignore_symbols = occurring_symbols.intersection(ignore_symbols)

    if len(occuring_ignore_symbols) > 0:
      logger.info(
        f"Removing {n_gram}-grams which contain: {' '.join(list(sorted(occuring_ignore_symbols)))}...")
      available_ngrams: OrderedDictType[int, List[Tuple]] = OrderedDict({
        k: filter_ngrams(v, occuring_ignore_symbols) for k, v in available_ngrams.items()
      })

      new_occurring_ngrams = {x for y in available_ngrams.values() for x in y}
      new_occurring_ngrams_count = len(new_occurring_ngrams)

      logger.info(
          f"Removed {occurring_ngrams_count - new_occurring_ngrams_count} unique {n_gram}-gram(s).")

  return available_ngrams


def get_first_percent(data: OrderedSet, percent: float) -> OrderedSet:
  proportion = len(data) / 100 * percent
  # rounding is strange see: https://docs.python.org/3/library/functions.html#round
  percent_count = round(proportion)
  res = data[:percent_count]
  return res

# def ignore_ngrams(available_ngrams: OrderedDictType[int, List[Tuple]], ignore_symbols: Set[str]):
#   logger = getLogger(__name__)
#   if len(ignore_symbols) > 0:
#     occurring_ngrams = {x for y in available_ngrams.values() for x in y}
#     occurring_ngrams_count = len(occurring_ngrams)
#     logger.info(
#       f"Removing entries which contain any of these symbols: {' '.join(list(sorted(ignore_symbols)))}...")
#     available_ngrams: OrderedDictType[int, List[Tuple]] = OrderedDict({
#       k: filter_ngrams(v, ignore_symbols) for k, v in available_ngrams.items()
#     })

#     new_occurring_ngrams = {x for y in available_ngrams.values() for x in y}
#     new_occurring_ngrams_count = len(new_occurring_ngrams)
#     logger.info(
#         f"Removed {occurring_ngrams_count - new_occurring_ngrams_count} unique {n_gram}-gram(s).")
