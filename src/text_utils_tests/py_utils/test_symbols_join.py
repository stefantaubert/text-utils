from text_utils.utils import symbols_join


def test_empty_list__returns_empty_tuple():
  symbols_list = []

  res = symbols_join(symbols_list, join_symbol=" ")

  assert res == tuple()


def test_one_symbol__returns_symbol_as_tuple():
  symbols_list = [("a",)]

  res = symbols_join(symbols_list, join_symbol=" ")

  assert res == ("a",)


def test_two_symbols_join_with_space__returns_both_symbols_separated_by_space():
  words = [("a",), ("b",)]

  res = symbols_join(words, join_symbol=" ")

  assert res == ("a", " ", "b")


def test_two_symbols_join_with_empty__returns_both_symbols_separated_by_empty():
  words = [("a",), ("b",)]

  res = symbols_join(words, join_symbol="")

  assert res == ("a", "", "b")


def test_two_empty_join_with_space__returns_both_empty_separated_by_space():
  words = [("",), ("",)]

  res = symbols_join(words, join_symbol=" ")

  assert res == ("", " ", "")


def test_two_empty_join_with_empty__returns_both_empty_separated_by_empty():
  words = [("",), ("",)]

  res = symbols_join(words, join_symbol="")

  assert res == ("", "", "")
