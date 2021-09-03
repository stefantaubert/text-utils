from collections import OrderedDict
from typing import OrderedDict as OrderedDictType
from typing import Set, Union

from text_utils.types import Accent, AccentId, AccentIds, Accents
from text_utils.utils import (deserialize_list, get_entries_ids_dict_order,
                              parse_json, save_json, serialize_list)


class AccentsDict():
  def __init__(self, ids_to_accents: OrderedDictType[Accent, AccentId]):
    super().__init__()
    self._ids_to_accents = ids_to_accents

  def save(self, file_path: str):
    save_json(file_path, self._ids_to_accents)

  @classmethod
  def from_raw(cls, raw: OrderedDictType[Accent, AccentId]):
    return cls(raw)

  def raw(self) -> OrderedDictType[Accent, AccentId]:
    return self._ids_to_accents

  def id_exists(self, accent_id: AccentId) -> bool:
    return accent_id in self._ids_to_accents.values()

  def get_id(self, accent: str) -> AccentId:
    assert accent in self._ids_to_accents.keys()
    return self._ids_to_accents[accent]

  def get_accent(self, accent_id: AccentId) -> str:
    assert accent_id in self._ids_to_accents.values()
    for accent, a_id in self._ids_to_accents.items():
      if a_id == accent_id:
        return accent
    assert False

  def remove_ids(self, ids: Set[AccentId]) -> None:
    for accent_id in ids:
      accent = self.get_accent(accent_id)
      self._ids_to_accents.pop(accent)

  def get_all_accents(self) -> Set[Accent]:
    return set(self._ids_to_accents.keys())

  def get_all_ids(self) -> Set[AccentId]:
    return set(self._ids_to_accents.values())

  def get_ids(self, accents: Accents) -> AccentIds:
    ids = tuple(self.get_id(accent) for accent in accents)
    return ids

  def get_accents(self, accent_ids: Union[str, AccentIds]) -> Accents:
    if isinstance(accent_ids, str):
      accent_ids = tuple(deserialize_list(accent_ids))
    elif not isinstance(accent_ids, tuple):
      assert False
    accents = tuple(self.get_accent(accent_id) for accent_id in accent_ids)
    return accents

  def get_serialized_ids(self, accents: Accents) -> str:
    ids = self.get_ids(accents)
    return serialize_list(ids)

  def __len__(self):
    return len(self._ids_to_accents)

  @classmethod
  def load(cls, file_path: str):
    data = parse_json(file_path)
    loaded = OrderedDict(data.items())
    return cls.from_raw(loaded)

  @classmethod
  def init_from_accents(cls, accents: Set[Accent]):
    unique_entries = list(sorted(accents))
    ids_to_accents = get_entries_ids_dict_order(unique_entries)
    return cls.from_raw(ids_to_accents)

  @classmethod
  def init_from_accents_with_pad(cls, accents: Set[Accent], pad_accent: Accent):
    unique_entries = list(sorted(accents - {pad_accent}))
    final_accents = [pad_accent] + unique_entries
    ids_to_accents = get_entries_ids_dict_order(final_accents)
    return cls.from_raw(ids_to_accents)
