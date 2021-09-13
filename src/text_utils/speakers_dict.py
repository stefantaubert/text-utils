from collections import Counter, OrderedDict
from pathlib import Path
from typing import OrderedDict as OrderedDictType
from typing import Set

from text_utils.types import Speaker, SpeakerId, SpeakerIds, Speakers
from text_utils.utils import parse_json, save_json, switch_keys_with_values


class SpeakersDict(OrderedDict):  # [Speaker, SpeakerId]
  def save(self, file_path: Path):
    save_json(file_path, self.raw())

  def get_all_speakers(self) -> Speakers:
    return list(self.keys())

  def get_all_speaker_ids(self) -> SpeakerIds:
    return list(self.values())

  def remove_ids(self, ids: Set[SpeakerId]) -> None:
    pop_keys: Set[str] = set()
    for speaker_name, speaker_id in self.items():
      if speaker_id in ids:
        pop_keys |= {speaker_name}

    for pop_key in pop_keys:
      self.pop(pop_key)

  def get_id(self, speaker: Speaker) -> SpeakerId:
    result = self[speaker]
    return result

  def get_speaker(self, speaker_id: SpeakerId) -> Speaker:
    result = switch_keys_with_values(self)[speaker_id]
    return result

  def id_exists(self, speaker_id: SpeakerId) -> bool:
    return speaker_id in self.values()

  def raw(self) -> OrderedDictType[Speaker, SpeakerId]:
    return OrderedDict(self)

  @classmethod
  def from_raw(cls, raw: OrderedDictType[Speaker, SpeakerId]):
    return cls(raw)

  @classmethod
  def load(cls, file_path: Path):
    data = parse_json(file_path)
    loaded = OrderedDict(data.items())
    return cls.from_raw(loaded)

  @classmethod
  def fromlist(cls, speakers: Speakers):
    res = [(x, i) for i, x in enumerate(speakers)]
    return cls(res)


class SpeakersLogDict(OrderedDict):  # [str, int]
  def save(self, file_path: Path):
    save_json(file_path, self)

  @classmethod
  def fromcounter(cls, counter: Counter):
    return cls(counter.most_common())
