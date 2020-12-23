import json
import os
from collections import OrderedDict
from typing import Dict, List
from typing import OrderedDict as OrderedDictType
from typing import Set, TypeVar

T = TypeVar('T')


def parse_json(path: str) -> Dict:
  assert os.path.isfile(path)
  with open(path, 'r', encoding='utf-8') as f:
    tmp = json.load(f)
  return tmp


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
