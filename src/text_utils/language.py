from enum import IntEnum


class Language(IntEnum):
  ENG = 0
  CHN = 1
  GER = 2

  def __repr__(self):
    if self == self.ENG:
      return str("English")
    if self == self.CHN:
      return str("Chinese")
    if self == self.GER:
      return str("German")
    assert False

  def __str__(self):
    if self == self.ENG:
      return str("ENG")
    if self == self.CHN:
      return str("CHN")
    if self == self.GER:
      return str("GER")
    assert False


lang_dict = {str(x): x for x in list(Language)}


def is_lang_from_str_supported(lang: str) -> bool:
  return lang in lang_dict


def get_lang_from_str(lang: str) -> Language:
  assert is_lang_from_str_supported(lang)
  return lang_dict[lang]
