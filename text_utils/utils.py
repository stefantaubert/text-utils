import json
import os
from collections import OrderedDict
from typing import Dict, List
from typing import OrderedDict as OrderedDictType
from typing import Set, Tuple, TypeVar, Union

from ordered_set import OrderedSet

T = TypeVar('T')


_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")


def parse_json(path: str) -> Dict:
  assert os.path.isfile(path)
  with open(path, 'r', encoding='utf-8') as f:
    tmp = json.load(f)
  return tmp


def filter_ngrams(ngrams: List[Tuple[_T2]], ignore_symbol_ids: Set[_T1]) -> List[Tuple]:
  res = [x for x in ngrams if len(set(x).intersection(ignore_symbol_ids)) == 0]
  return res


def save_json(path: str, mapping_dict: dict) -> None:
  with open(path, 'w', encoding='utf-8') as f:
    json.dump(mapping_dict, f, ensure_ascii=False, indent=2)


def deserialize_list(serialized_str: str) -> List[int]:
  sentences_symbols = serialized_str.split(',')
  sentences_symbols = list(map(int, sentences_symbols))
  return sentences_symbols


def serialize_list(symbol_ids: List[int]) -> str:
  sentences_symbols = list(map(str, symbol_ids))
  sentences_symbols = ','.join(sentences_symbols)
  return sentences_symbols


def get_entries_ids_dict(symbols: Set[str]) -> OrderedDictType[str, int]:
  unique_symbols = list(sorted(set(symbols)))
  return get_entries_ids_dict_order(unique_symbols)


def get_entries_ids_dict_order(symbols: List[str]) -> OrderedDictType[str, int]:
  assert len(symbols) == len(set(symbols))
  res = OrderedDict([(s, i) for i, s in enumerate(symbols)])
  return res


def switch_keys_with_values(dictionary: OrderedDictType) -> OrderedDictType:
  result = OrderedDict([(v, k) for k, v in dictionary.items()])
  return result


def get_sorted_list_from_set(unsorted_set: Set[T]) -> List[T]:
  res: List[T] = list(sorted(list(unsorted_set)))
  return res


def get_basename(filepath: str) -> str:
  '''test.wav -> test'''
  basename, _ = os.path.splitext(os.path.basename(filepath))
  return basename


def values_to_set(d: OrderedDictType[_T1, _T2]) -> OrderedDictType[_T1, _T2]:
  res: OrderedDictType[_T1, _T2] = OrderedDict({k: set(v) for k, v in d.items()})
  return res


def filter_entries_from_lists(d: OrderedDictType[_T1, List[_T2]], allowed_entries: Set[_T2]) -> OrderedDictType[_T1, List[_T2]]:
  res = OrderedDict({k: [x for x in v if x in allowed_entries] for k, v in d.items()})
  return res


def get_until_sum(d: OrderedDictType[_T1, _T2], until_values: Dict[_T1, Union[float, int]], until_value: Union[float, int]) -> OrderedDictType[_T1, _T2]:
  total = 0
  res: OrderedDictType[_T1, _T2] = OrderedDict()
  for k, v in d.items():
    current_val = until_values[k]
    include = total + current_val < until_value
    if not include:
      break
    res[k] = v
    total += current_val

  return res


def get_first_n(d: OrderedDictType[_T1, _T2], n: int) -> OrderedDictType[_T1, _T2]:
  assert n >= 0
  first_keys = set(list(d.keys())[:n])
  res: OrderedDictType[_T1, _T2] = OrderedDict({k: v for k, v in d.items() if k in first_keys})
  return res


def select_enties_from_ordereddict(select_from: OrderedDictType[_T1, _T2], keys: Set[_T1]) -> OrderedDictType[_T1, _T2]:
  keys_exist = len(keys.difference(select_from.keys())) == 0
  assert keys_exist
  res: OrderedDictType[_T1, _T2] = OrderedDict({k: v for k, v in select_from.items() if k in keys})
  return res
