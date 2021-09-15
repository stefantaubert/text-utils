from text_utils.symbol_format import SymbolFormat, get_format_from_str


def test_get_format_from_str():
  result = get_format_from_str("PHONES_IPA")

  assert result == SymbolFormat.PHONES_IPA
