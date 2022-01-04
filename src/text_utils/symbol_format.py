from enum import IntEnum


class SymbolFormat(IntEnum):
  PHONES_IPA = 0
  PHONEMES_IPA = 1
  PHONEMES_ARPA = 2
  GRAPHEMES = 3

  def __repr__(self):
    if self == self.PHONES_IPA:
      return str("Phones (IPA)")
    if self == self.PHONEMES_IPA:
      return str("Phonemes (IPA)")
    if self == self.PHONEMES_ARPA:
      return str("Phonemes (ARPA)")
    if self == self.GRAPHEMES:
      return str("Graphemes")
    assert False

  def __str__(self):
    if self == self.PHONES_IPA:
      return str("PHONES_IPA")
    if self == self.PHONEMES_IPA:
      return str("PHONEMES_IPA")
    if self == self.PHONEMES_ARPA:
      return str("PHONEMES_ARPA")
    if self == self.GRAPHEMES:
      return str("GRAPHEMES")
    assert False

  @property
  def is_IPA(self):
    return self in (self.PHONEMES_IPA, self.PHONES_IPA)

  @property
  def is_ARPA(self):
    return self in (self.PHONEMES_ARPA)


format_dict = {str(x): x for x in list(SymbolFormat)}


def is_symbol_format_from_str_supported(symbol_format: str) -> bool:
  return symbol_format in format_dict


def get_format_from_str(symbol_format: str) -> SymbolFormat:
  assert is_symbol_format_from_str_supported(symbol_format)
  return format_dict[symbol_format]
