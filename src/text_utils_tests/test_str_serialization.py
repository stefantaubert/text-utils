from text_utils.str_serialization import str_deserialization, str_serialization

# region str_deserialization


def test_str_serialization__single_non_split_symbol():
  symbols = ("a",)
  res = str_serialization(symbols, " ")

  assert res == "a"


def test_str_serialization__two_symbols_no_split_symbol():
  symbols = ("a", "a")
  res = str_serialization(symbols, " ")

  assert res == "a a"


def test_str_serialization__symbol_split_symbol_symbol():
  symbols = ("a", " ", "a")
  res = str_serialization(symbols, " ")

  assert res == "a   a"


def test_str_serialization__one_symbol_consists_of_two_chars():
  symbols = ("ab", "a")
  res = str_serialization(symbols, " ")

  assert res == "ab a"


def test_str_serialization__split_symbol_at_end():
  symbols = ("a", "a", " ")
  res = str_serialization(symbols, " ")

  assert res == "a a  "


def test_str_serialization__split_symbol_at_beginning():
  symbols = (" ", "a", "a")
  res = str_serialization(symbols, " ")

  assert res == "  a a"


def test_str_serialization__only_one_split_symbol():
  symbols = (" ",)
  res = str_serialization(symbols, " ")

  assert res == " "


def test_str_serialization__only_two_split_symbols():
  symbols = (" ", " ")
  res = str_serialization(symbols, " ")

  assert res == "   "


def test_str_serialization__only_three_split_symbols():
  symbols = (" ", " ", " ")
  res = str_serialization(symbols, " ")

  assert res == "     "


def test_str_serialization__symbols_is_empty():
  symbols = ()
  res = str_serialization(symbols, " ")

  assert res == ""

# endregion

# region str_deserialization


def test_str_deserialization__component_test():
  text = "  a ab   a  "
  res = list(str_deserialization(text, " "))

  assert res == [" ", "a", "ab", " ", "a", " "]


def test_str_deserialization_three_spaces():
  text = "a     a"
  res = list(str_deserialization(text, " "))

  assert res == ["a", " ", " ", "a"]


def test_str_deserialization_five_spaces():
  text = "a     a"
  res = list(str_deserialization(text, " "))

  assert res == ["a", " ", " ", "a"]


def test_str_deserialization_seven_spaces():
  text = "a       a"
  res = list(str_deserialization(text, " "))

  assert res == ["a", " ", " ", " ", "a"]


def test_str_deserialization_two_spaces_at_end():
  text = "a  "
  res = list(str_deserialization(text, " "))

  assert res == ["a", " "]


def test_str_deserialization_two_spaces_at_beginning():
  text = "  a"
  res = list(str_deserialization(text, " "))

  assert res == [" ", "a"]


def test_str_deserialization_only_spaces():
  text = "   "
  res = list(str_deserialization(text, " "))

  assert res == [" ", " "]


def test_str_deserialization_empty_text():
  text = ""
  res = list(str_deserialization(text, " "))

  assert res == []

# endregion
