from text_utils.string_format import convert_symbols_to_symbols_string


def test_component():
  symbols = (" ", "a", " ", "b", "c", " ", "d", "ef", "g", " ", " ", "h", "i", " ")
  result = convert_symbols_to_symbols_string(symbols)
  assert result == "  a  b c  d ef g    h i  "


def test_empty__returns_empty():
  assert convert_symbols_to_symbols_string(tuple()) == ""


def test_one_symbol__returns_symbol():
  assert convert_symbols_to_symbols_string(("a",)) == "a"


def test_two_symbols__returns_symbols():
  assert convert_symbols_to_symbols_string(("a", "b")) == "a b"


def test_one_doublesymbol__returns_doublesymbol():
  assert convert_symbols_to_symbols_string(("ab",)) == "ab"


def test_space__returns_doublespace():
  assert convert_symbols_to_symbols_string((" ",)) == "  "


def test_two_spaces__returns_quadspace():
  assert convert_symbols_to_symbols_string((" ", " ")) == "    "


def test_symbol_after_space__returns_doublespace_and_symbol():
  assert convert_symbols_to_symbols_string((" ", "a")) == "  a"


def test_symbol_before_space__returns_symbol_and_doublespace():
  assert convert_symbols_to_symbols_string(("a", " ")) == "a  "


def test_symbol_before_and_after_space__returns_symbol_and_doublespace_and_symbol():
  assert convert_symbols_to_symbols_string(("a", " ", "a")) == "a  a"
