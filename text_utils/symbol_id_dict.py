import os
from collections import OrderedDict
from shutil import copyfile
from typing import List, Optional
from typing import OrderedDict as OrderedDictType
from typing import Set, Union

from utils import (deserialize_list, get_basename, get_entries_ids_dict_order,
                   parse_json, save_json, serialize_list,
                   switch_keys_with_values)


class SymbolIdDict():
  def __init__(self, ids_to_symbols: OrderedDictType[str, int]):
    super().__init__()
    self._ids_to_symbols = ids_to_symbols
    self._symbols_to_ids = switch_keys_with_values(ids_to_symbols)

  @staticmethod
  def symbols_to_text(symbols: List[str]) -> str:
    return ''.join(symbols)

  @staticmethod
  def deserialize_symbol_ids(serialized_str: str):
    return deserialize_list(serialized_str)

  @staticmethod
  def serialize_symbol_ids(symbol_ids: list):
    return serialize_list(symbol_ids)

  @classmethod
  def from_raw(cls, raw: OrderedDictType[str, int]):
    return cls(raw)

  def raw(self) -> OrderedDictType[str, int]:
    return self._ids_to_symbols

  def __len__(self):
    return len(self._ids_to_symbols)

  def get_symbol(self, symbol_id: int):
    assert symbol_id in self._symbols_to_ids.keys()
    return self._symbols_to_ids[symbol_id]

  def id_exists(self, symbol_id: int) -> bool:
    return symbol_id in self._ids_to_symbols.values()

  def symbol_exists(self, symbol: str) -> bool:
    return symbol in self._ids_to_symbols.keys()

  def get_id(self, symbol: str):
    assert symbol in self._ids_to_symbols.keys()
    return self._ids_to_symbols[symbol]

  def get_all_symbols(self) -> Set[str]:
    return set(self._ids_to_symbols.keys())

  def get_all_symbol_ids(self) -> Set[int]:
    return set(self._ids_to_symbols.values())

  def remove_ids(self, ids: Set[int]) -> None:
    for symbol_id in ids:
      self._symbols_to_ids.pop(symbol_id)
    self._ids_to_symbols = switch_keys_with_values(self._symbols_to_ids)

  def save(self, file_path: str):
    save_json(file_path, self._ids_to_symbols)

  def replace_unknown_symbols_with_pad(self, symbols: List[str], pad_symbol: Optional[str] = "_") -> List[str]:
    assert pad_symbol in self._ids_to_symbols.keys()
    result = []
    for symbol in symbols:
      if symbol in self._ids_to_symbols.keys():
        result.append(symbol)
      else:
        result.append(pad_symbol)
    return result

  def has_unknown_symbols(self, symbols: List[str]) -> bool:
    for symbol in symbols:
      if not self.symbol_exists(symbol):
        return True
    return False

  def get_ids(self, symbols: List[str]) -> List[int]:
    ids = [self.get_id(symbol) for symbol in symbols]
    return ids

  def get_serialized_ids(self, symbols: List[str]) -> str:
    return serialize_list(self.get_ids(symbols))

  def get_symbols(self, symbol_ids: Union[str, List[int]]) -> List[str]:
    if isinstance(symbol_ids, str):
      symbol_ids = deserialize_list(symbol_ids)
    elif not isinstance(symbol_ids, list):
      assert False
    symbols = [self.get_symbol(s_id) for s_id in symbol_ids]
    return symbols

  # def serialized_symbol_ids_to_text(self, serialized_symbol_ids: str):
  #   symbol_ids = SymbolIdDict.deserialize_symbol_ids(serialized_symbol_ids)
  #   return self.get_text(symbol_ids)

  def get_text(self, symbol_ids: Union[str, List[int]]) -> str:
    symbols = self.get_symbols(symbol_ids)
    return SymbolIdDict.symbols_to_text(symbols)

  @classmethod
  def load_from_file(cls, filepath: str):
    loaded = parse_json(filepath)
    loaded = OrderedDict(loaded.items())
    values = list(loaded.values())
    assert len(values) > 0
    is_v2 = isinstance(values[0], list)
    if is_v2:
      tmp = [(data[1], int(symbol_id)) for symbol_id, data in loaded.items()]
      tmp.sort(key=lambda x: x[1])
      ids_to_symbols = OrderedDict(tmp)
      file_name = get_basename(filepath)
      backup_path = os.path.join(os.path.dirname(filepath), f"{file_name}.v2.json")
      copyfile(filepath, backup_path)
      res = cls.from_raw(ids_to_symbols)
      res.save(filepath)
      return res
    ids_to_symbols = loaded
    return cls.from_raw(ids_to_symbols)

  @classmethod
  def init_from_symbols(cls, symbols: Set[str]):
    unique_entries = list(sorted(symbols))
    ids_to_symbols = get_entries_ids_dict_order(unique_entries)
    return cls(ids_to_symbols)

  @classmethod
  def init_from_symbols_with_pad(cls, symbols: Set[str], pad_symbol: str = "_"):
    unique_entries = list(sorted(symbols - {pad_symbol}))
    final_symbols = [pad_symbol] + unique_entries
    ids_to_symbols = get_entries_ids_dict_order(final_symbols)
    return cls(ids_to_symbols)

# if __name__ == "__main__":
#   res = SymbolIdDict.load_from_file("/tmp/symbols.v2.json")
#   print(res)
