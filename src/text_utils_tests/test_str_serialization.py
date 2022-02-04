from text_utils.str_serialization import (can_deserialize_symbols, can_serialize_symbols,
                                          deserialize_symbols,
                                          serialize_symbols)

# region str_deserialization


def test_str_serialization__single_non_split_symbol():
  symbols = ("a",)
  res = serialize_symbols(symbols, " ")

  assert res == "a"


def test_str_serialization__two_symbols_no_split_symbol():
  symbols = ("a", "a")
  res = serialize_symbols(symbols, " ")

  assert res == "a a"


def test_str_serialization__symbol_split_symbol_symbol():
  symbols = ("a", " ", "a")
  res = serialize_symbols(symbols, " ")

  assert res == "a   a"


def test_str_serialization__one_symbol_consists_of_two_chars():
  symbols = ("ab", "a")
  res = serialize_symbols(symbols, " ")

  assert res == "ab a"


def test_str_serialization__split_symbol_at_end():
  symbols = ("a", "a", " ")
  res = serialize_symbols(symbols, " ")

  assert res == "a a  "


def test_str_serialization__split_symbol_at_beginning():
  symbols = (" ", "a", "a")
  res = serialize_symbols(symbols, " ")

  assert res == "  a a"


def test_str_serialization__only_one_split_symbol():
  symbols = (" ",)
  res = serialize_symbols(symbols, " ")

  assert res == " "


def test_str_serialization__only_two_split_symbols():
  symbols = (" ", " ")
  res = serialize_symbols(symbols, " ")

  assert res == "   "


def test_str_serialization__only_three_split_symbols():
  symbols = (" ", " ", " ")
  res = serialize_symbols(symbols, " ")

  assert res == "     "


def test_str_serialization__symbols_is_empty():
  symbols = ()
  res = serialize_symbols(symbols, " ")

  assert res == ""

# endregion

# region str_deserialization


def test_str_deserialization__component_test():
  text = "  a ab   a  "
  res = list(deserialize_symbols(text, " "))

  assert res == [" ", "a", "ab", " ", "a", " "]


def test_str_deserialization_three_spaces():
  text = "a     a"
  res = list(deserialize_symbols(text, " "))

  assert res == ["a", " ", " ", "a"]


def test_str_deserialization_five_spaces():
  text = "a     a"
  res = list(deserialize_symbols(text, " "))

  assert res == ["a", " ", " ", "a"]


def test_str_deserialization_seven_spaces():
  text = "a       a"
  res = list(deserialize_symbols(text, " "))

  assert res == ["a", " ", " ", " ", "a"]


def test_str_deserialization_two_spaces_at_end():
  text = "a  "
  res = list(deserialize_symbols(text, " "))

  assert res == ["a", " "]


def test_str_deserialization_two_spaces_at_beginning():
  text = "  a"
  res = list(deserialize_symbols(text, " "))

  assert res == [" ", "a"]


def test_str_deserialization_four_spaces_at_end():
  text = "a    "
  res = list(deserialize_symbols(text, " "))

  assert res == ["a", " ", " "]


def test_str_deserialization_four_spaces_at_beginning():
  text = "    a"
  res = list(deserialize_symbols(text, " "))

  assert res == [" ", " ", "a"]


def test_str_deserialization_only_one_space():
  text = " "
  res = list(deserialize_symbols(text, " "))

  assert res == [" "]


def test_str_deserialization_only_three_spaces():
  text = "   "
  res = list(deserialize_symbols(text, " "))

  assert res == [" ", " "]


def test_str_deserialization_only_five_spaces():
  text = "     "
  res = list(deserialize_symbols(text, " "))

  assert res == [" ", " ", " "]


def test_str_deserialization_empty_text():
  text = ""
  res = list(deserialize_symbols(text, " "))

  assert res == []

# endregion

# region can_deserialize

# spaces in middle


def test_can_deserialize__one_space_in_between():
  text = "a b"
  res = can_deserialize_symbols(text, " ")

  assert res


def test_can_deserialize__two_spaces_in_between():
  text = "a  b"
  res = can_deserialize_symbols(text, " ")

  assert not res


def test_can_deserialize__three_spaces_in_between():
  text = "a   b"
  res = can_deserialize_symbols(text, " ")

  assert res


def test_can_deserialize__four_spaces_in_between():
  text = "a    b"
  res = can_deserialize_symbols(text, " ")

  assert not res


def test_can_deserialize__five_spaces_in_between():
  text = "a     b"
  res = can_deserialize_symbols(text, " ")

  assert res

# spaces at beginning


def test_can_deserialize__one_space_at_beginning():
  text = " a"
  res = can_deserialize_symbols(text, " ")

  assert not res


def test_can_deserialize__two_spaces_at_beginning():
  text = "  a"
  res = can_deserialize_symbols(text, " ")

  assert res


def test_can_deserialize__three_spaces_at_beginning():
  text = "   a"
  res = can_deserialize_symbols(text, " ")

  assert not res


def test_can_deserialize__four_spaces_at_beginning():
  text = "    a"
  res = can_deserialize_symbols(text, " ")

  assert res


def test_can_deserialize__five_spaces_at_beginning():
  text = "     a"
  res = can_deserialize_symbols(text, " ")

  assert not res

# spaces at end


def test_can_deserialize__one_space_at_end():
  text = "a "
  res = can_deserialize_symbols(text, " ")

  assert not res


def test_can_deserialize__two_spaces_at_end():
  text = "a  "
  res = can_deserialize_symbols(text, " ")

  assert res


def test_can_deserialize__three_spaces_at_end():
  text = "a   "
  res = can_deserialize_symbols(text, " ")

  assert not res


def test_can_deserialize__four_spaces_at_end():
  text = "a    "
  res = can_deserialize_symbols(text, " ")

  assert res


def test_can_deserialize__five_spaces_at_end():
  text = "a     "
  res = can_deserialize_symbols(text, " ")

  assert not res

# endregion

# region can_serialize


def test_can_serialize():
  symbols = ("a", " ")
  res = can_serialize_symbols(symbols, " ")

  assert res == True


def test_can_serialize__expect_false():
  symbols = ("a ",)
  res = can_serialize_symbols(symbols, " ")

  assert res == False

# endregion
