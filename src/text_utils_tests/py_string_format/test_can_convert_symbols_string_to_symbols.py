
from text_utils.string_format import can_convert_symbols_string_to_symbols


def test_component__returns_true():
  assert can_convert_symbols_string_to_symbols("  t h is  i s    te st .  ")

def test_component__returns_false():
  assert not can_convert_symbols_string_to_symbols("t   h is")


def test_empty__returns_true():
  assert can_convert_symbols_string_to_symbols("")


def test_one_symbol__returns_true():
  assert can_convert_symbols_string_to_symbols("a")


def test_two_symbols_sep_by_space__returns_true():
  assert can_convert_symbols_string_to_symbols("a a")


def test_two_symbols_sep_by_two_spaces__returns_true():
  assert can_convert_symbols_string_to_symbols("a  a")


def test_two_symbols_sep_by_three_spaces__returns_false():
  assert not can_convert_symbols_string_to_symbols("a   a")


def test_space__returns_false():
  assert not can_convert_symbols_string_to_symbols(" ")


def test_double_space__returns_true():
  assert can_convert_symbols_string_to_symbols("  ")


def test_triplespace__returns_false():
  assert not can_convert_symbols_string_to_symbols("   ")


def test_quadspace__returns_true():
  assert can_convert_symbols_string_to_symbols("    ")
