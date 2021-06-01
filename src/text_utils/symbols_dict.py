from collections import Counter, OrderedDict

from text_utils.utils import parse_json, save_json


class SymbolsDict(OrderedDict):  # Tuple[str, int]
  def save(self, file_path: str):
    save_json(file_path, self)

  @classmethod
  def load(cls, file_path: str):
    data = parse_json(file_path)
    return cls(data)

  @classmethod
  def fromcounter(cls, counter: Counter):
    return cls(counter.most_common())
