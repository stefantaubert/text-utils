from text_utils.utils import (delete_and_insert_in_list, is_sublist,
                              symbols_join, symbols_replace, symbols_split,
                              symbols_strip, symbols_to_lower,
                              upper_list_if_true)


def test_sentence_to_words__empty_list():
  sentence = []

  res = symbols_split(sentence, split_symbol=" ")

  assert res == []


def test_sentence_to_words__only_one_space():
  sentence = (" ")

  res = symbols_split(sentence, split_symbol=" ")

  assert res == [(), ()]


def test_sentence_to_words__one_word():
  sentence = ("a")

  res = symbols_split(sentence, split_symbol=" ")

  assert res == [("a",)]


def test_sentence_to_words__two_words():
  sentence = ("a", " ", "b",)

  res = symbols_split(sentence, split_symbol=" ")

  assert res == [("a",), ("b",)]


def test_words_to_sentence__empty_list():
  words = []

  res = symbols_join(words, join_symbol=" ")

  assert res == ()


def test_words_to_sentence__one_word():
  words = [("a",)]

  res = symbols_join(words, join_symbol=" ")

  assert res == ("a",)


def test_words_to_sentence__two_words():
  words = [("a",), ("b",)]

  res = symbols_join(words, join_symbol=" ")

  assert res == ("a", " ", "b")


def test_strip_word__empty_word():
  word = ()

  res = symbols_strip(word, strip={"a"})
  assert res == ()


def test_strip_word__empty_strip():
  word = ("a",)

  res = symbols_strip(word, strip=[])

  assert res == ("a",)


def test_strip_word__strip_start():
  word = ("a", "b",)

  res = symbols_strip(word, strip={"a"})

  assert res == ("b",)


def test_strip_word__strip_end():
  word = ("a", "b",)

  res = symbols_strip(word, strip={"b"})

  assert res == ("a",)


def test_strip_word__strip_start_and_end():
  word = ("b", "a", "b",)

  res = symbols_strip(word, strip={"b"})

  assert res == ("a",)


def test_strip_word__strip_start_and_end_multiple_symbols():
  word = ("b", "c", "a", "e", "b", "d",)

  res = symbols_strip(word, strip={"b", "c", "d"})

  assert res == ("a", "e",)


def test_strip_word__strip_not_inside():
  word = ("a", "b", "a",)

  res = symbols_strip(word, strip={"b"})

  assert res == ("a", "b", "a",)


def test_symbols_to_lower():
  res = symbols_to_lower(("A", "a", "B",))
  assert res == ("a", "a", "b",)


# region upper_list_if_true


def test_upper_list_if_true__upper_is_false():
  test_list = ["ABC", "abc", "Abc", "aBC"]
  res = upper_list_if_true(test_list, False)

  assert res == test_list


def test_upper_list_if_true__upper_is_true():
  test_list = ["ABC", "abc", "Abc", "aBC"]
  res = upper_list_if_true(test_list, True)

  assert res == ["ABC", "ABC", "ABC", "ABC"]

# endregion

# region is_sublist


def test_is_sublist__two_equal_lists__return_0():
  search_in = ["abc"]
  search_for = ["abc"]
  res = is_sublist(search_in, search_for, False)

  assert res == 0


def test_is_sublist__is_not_sublist():
  search_in = ["abc", "def", "HIJ", "KLM"]
  search_for = ["123", "HIJ", "KLM"]
  res = is_sublist(search_in, search_for, True)

  assert res == -1


def test_is_sublist__is_sublist_ignore_case_is_true():
  search_in = ["abc", "def", "HIJ", "KLM"]
  search_for = ["hij", "KLm"]
  res = is_sublist(search_in, search_for, True)

  assert res == 2


def test_is_sublist__is_not_sublist_ignore_case_is_false():
  search_in = ["abc", "def", "HIJ", "KLM"]
  search_for = ["HIJ", "KLm"]
  res = is_sublist(search_in, search_for, False)

  assert res == -1


def test_is_sublist__is_sublist_ignore_case_is_false():
  search_in = ["abc", "def", "HIj", "kLM"]
  search_for = ["HIj", "kLM"]
  res = is_sublist(search_in, search_for, False)

  assert res == 2


def test_is_sublist__is_sublist_ensure_first_finding_is_returned():
  search_in = ["abc", "def", "hij", "klm", "hij", "klm"]
  search_for = ["HIj", "kLM"]
  res = is_sublist(search_in, search_for, True)

  assert res == 2

# endregion

# region delete_and_insert_in_list


def test_delete_and_insert_in_list__at_beginning():
  main_list = ["abc", "def", "hij", "klm"]
  list_to_delete = ["abc", "def"]
  list_to_insert = ["123"]
  delete_and_insert_in_list(main_list, list_to_delete, list_to_insert, 0)

  assert main_list == ["123", "hij", "klm"]


def test_delete_and_insert_in_list__at_end():
  main_list = ["abc", "def", "hij", "klm"]
  list_to_delete = ["klm"]
  list_to_insert = ["123", "456"]
  delete_and_insert_in_list(main_list, list_to_delete, list_to_insert, 3)

  assert main_list == ["abc", "def", "hij", "123", "456"]


def test_delete_and_insert_in_list__in_middle():
  main_list = ["abc", "def", "hij", "klm"]
  list_to_delete = ["def", "hij"]
  list_to_insert = ["123"]
  delete_and_insert_in_list(main_list, list_to_delete, list_to_insert, 1)

  assert main_list == ["abc", "123", "klm"]

# endregion

# region symbols_replace


def test_symbols_replace__only_one_occurence():
  symbols = ("abc", "def", "hij", "klm",)
  search_for = ("def", "hij",)
  replace_with = ("123",)
  res = symbols_replace(symbols, search_for, replace_with, True)

  assert res == ("abc", "123", "klm",)


def test_symbols_replace__two_occurences():
  symbols = ("abc", "def", "hij", "klm", "def", "hij",)
  search_for = ("def", "hij",)
  replace_with = ("123",)
  res = symbols_replace(symbols, search_for, replace_with, True)

  assert res == ("abc", "123", "klm", "123",)


def test_symbols_replace__no_occurence():
  symbols = ("abc", "def", "hij", "klm",)
  search_for = ("deF", "hij",)
  replace_with = ("123",)
  res = symbols_replace(symbols, search_for, replace_with, False)

  assert res == ("abc", "def", "hij", "klm",)


def test_symbols_replace__replace_whole_list():
  symbols = ("abc", "def", "hij", "klm",)
  search_for = ("abc", "def", "hij", "klm",)
  replace_with = ("abcdefg", "hijklmnop",)
  res = symbols_replace(symbols, search_for, replace_with, False)

  assert res == ("abcdefg", "hijklmnop",)

# endregion
