import json
import os
import re
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List
from typing import OrderedDict as OrderedDictType
from typing import Set, TypeVar

from text_utils.types import Symbol, Symbols

T = TypeVar('T')


_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")


def parse_json(path: Path) -> Dict:
  assert path.is_file()
  with path.open(mode='r', encoding='utf-8') as f:
    tmp = json.load(f)
  return tmp


def save_json(path: Path, mapping_dict: dict) -> None:
  with path.open(mode='w', encoding='utf-8') as f:
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


def filter_entries_from_lists(d: OrderedDictType[_T1, List[_T2]], allowed_entries: Set[_T2]) -> OrderedDictType[_T1, List[_T2]]:
  res = OrderedDict({k: [x for x in v if x in allowed_entries] for k, v in d.items()})
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


def split_text(text: str, separators: List[str]) -> List[str]:
  pattern = "|".join(separators)
  sents = re.split(f'({pattern})', text)
  res = []
  for i, sent in enumerate(sents):
    if i % 2 == 0:
      res.append(sent)
      if i + 1 < len(sents):
        res[-1] += sents[i + 1]
  res = [x.strip() for x in res]
  res = [x for x in res if x]
  return res


def symbols_ignore(symbols: Symbols, ignore: Set[Symbol]) -> Symbols:
  res = tuple(symbol for symbol in symbols if symbol not in ignore)
  return res


def remove_symbols_inside(symbols: Symbols, ignore: Set[Symbols]) -> Symbols:
  result = []
  for symbol in symbols:
    symbol_replaced = symbol
    for ignore_symbol in ignore:
      symbol_replaced = symbol_replaced.replace(ignore_symbol, "")
    result.append(symbol_replaced)
  return tuple(result)


def remove_symbols_at_all_places(symbols: Symbols, ignore: Set[Symbol]) -> Symbols:
  symbols = symbols_ignore(symbols, ignore=ignore)
  symbols = remove_symbols_inside(symbols, ignore=ignore)
  return symbols


def symbols_split(sentence_symbols: Symbols, split_symbol: Symbol) -> List[Symbols]:
  if len(sentence_symbols) == 0:
    return []
  res = []
  current_word = []
  for symbol in sentence_symbols:
    if symbol == split_symbol:
      res.append(tuple(current_word))
      current_word = []
    else:
      current_word.append(symbol)
  res.append(tuple(current_word))
  return res


def symbols_strip(symbols: Symbols, strip: Set[Symbol]) -> Symbols:
  res = []
  # strip start
  for i, char in enumerate(symbols):
    if char in strip:
      continue
    res = symbols[i:]
    break

  # strip end
  for i in range(len(res)):
    char = res[-1 - i]
    if char in strip:
      continue
    res = res[:len(res) - i]
    break
  return tuple(res)


def symbols_to_lower(symbols: Symbols) -> Symbols:
  res = tuple(symbol.lower() for symbol in symbols)
  return res


def symbols_join(list_of_symbols: List[Symbols], join_symbol: Symbol) -> Symbols:
  res = []
  for i, word in enumerate(list_of_symbols):
    res.extend(word)
    is_last_word = i == len(list_of_symbols) - 1
    if not is_last_word:
      res.append(join_symbol)
  return tuple(res)


def symbols_replace(symbols: Symbols, search_for: Symbols, replace_with: Symbols, ignore_case: bool) -> Symbols:
  new_symbols = list(symbols)
  search_for_list = list(search_for)
  start_index = is_sublist(
      search_in=new_symbols,
      search_for=search_for_list,
      ignore_case=ignore_case
  )
  if start_index == -1:
    return tuple(new_symbols)

  delete_and_insert_in_list(
    main_list=new_symbols,
    list_to_delete=search_for_list,
    list_to_insert=replace_with,
    start_index=start_index
  )
  if is_sublist(
    search_in=new_symbols,
    search_for=search_for_list,
    ignore_case=ignore_case
  ) != -1:
    new_symbols = symbols_replace(new_symbols, search_for, replace_with, ignore_case)
  return tuple(new_symbols)


def delete_and_insert_in_list(main_list: List[str], list_to_delete: List[str], list_to_insert: List[str], start_index: int) -> None:
  del main_list[start_index:start_index + len(list_to_delete)]
  end_slice = main_list[start_index:]
  del main_list[start_index:]
  main_list.extend(list_to_insert)
  main_list.extend(end_slice)


def is_sublist(search_in: List[str], search_for: List[str], ignore_case: bool) -> int:
  len_search_in, len_search_for = len(search_in), len(search_for)
  aux_search_in = upper_list_if_true(search_in, ignore_case)
  aux_search_for = upper_list_if_true(search_for, ignore_case)
  for i in range(len_search_in):
    if aux_search_in[i:i + len_search_for] == aux_search_for:
      return i
  return -1


def upper_list_if_true(l: List[str], upper: bool) -> List[str]:
  if upper:
    upper_l = [element.upper() for element in l]
    return upper_l
  return l


def get_ngrams(symbols: Symbols, n: int) -> List[Symbols]:
  if n < 1:
    raise Exception()

  res: List[Symbols] = []
  for i in range(len(symbols) - n + 1):
    tmp = tuple(symbols[i:i + n])
    res.append(tmp)
  return res
