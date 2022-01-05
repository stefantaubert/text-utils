from text_utils.string_format import can_convert_symbols_to_symbols_string


def test_empty__returns_true():
  assert can_convert_symbols_to_symbols_string(tuple())


def test_one_symbol__returns_true():
  assert can_convert_symbols_to_symbols_string(("a",))


def test_two_symbols__returns_true():
  assert can_convert_symbols_to_symbols_string(("a", "b"))


def test_two_symbols_separated_by_space__returns_true():
  assert can_convert_symbols_to_symbols_string(("a", " ", "b"))


def test_one_space__returns_true():
  assert can_convert_symbols_to_symbols_string((" ",))


def test_two_spaces__returns_true():
  assert can_convert_symbols_to_symbols_string((" ", " "))


def test_one_doublespace__returns_false():
  assert not can_convert_symbols_to_symbols_string(("  ",))


def test_symbol_with_space__returns_false():
  assert not can_convert_symbols_to_symbols_string(("a ",))


def test_one_empty_symbol__returns_false():
  assert not can_convert_symbols_to_symbols_string(("",))


def test_symbol_and_empty_symbol__returns_false():
  assert not can_convert_symbols_to_symbols_string(("a", ""))
