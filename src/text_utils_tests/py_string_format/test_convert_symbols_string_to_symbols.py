from text_utils.string_format import convert_symbols_string_to_symbols


def test_component():
  result = convert_symbols_string_to_symbols("  a  b c  d ef g    h i  ")
  assert result == (" ", "a", " ", "b", "c", " ", "d", "ef", "g", " ", " ", "h", "i", " ")


def test_text_empty__returns_empty():
  result = convert_symbols_string_to_symbols("")
  assert result == tuple()


def test_text_one_char__returns_char_as_symbol():
  result = convert_symbols_string_to_symbols("e")
  assert result == ("e",)


def test_text_one_doublechar__returns_both_chars_as_symbol():
  result = convert_symbols_string_to_symbols("ee")
  assert result == ("ee",)


def test_text_one_word__returns_word_symbols():
  result = convert_symbols_string_to_symbols("t e s t")
  assert result == ("t", "e", "s", "t")


def test_text_two_words__returns_words_separated_by_space():
  result = convert_symbols_string_to_symbols("t e  a b")
  assert result == ("t", "e", " ", "a", "b")


def test_text_one_space__returns_space_symbol():
  result = convert_symbols_string_to_symbols("  ")
  assert result == (" ",)


def test_text_space_after_symbol__returns_symbol_and_space():
  result = convert_symbols_string_to_symbols("a  ")
  assert result == ("a", " ")


def test_text_space_before_symbol__returns_space_and_symbol():
  result = convert_symbols_string_to_symbols("  a")
  assert result == (" ", "a")


def test_text_space_before_and_after_symbol__returns_space_and_symbol_and_space():
  result = convert_symbols_string_to_symbols("  a  ")
  assert result == (" ", "a", " ")


def test_four_spaces__return_two_spaces():
  result = convert_symbols_string_to_symbols("    ")
  assert result == (" ", " ")
