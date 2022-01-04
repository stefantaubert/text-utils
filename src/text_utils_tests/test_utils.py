from text_utils.utils import (delete_and_insert_in_list, is_sublist,
                              remove_empty_symbols, remove_empty_symbols_list,
                              remove_space_around_punctuation,
                              split_symbols_on, 
                              symbols_map_outer, symbols_replace,
                              symbols_separate, symbols_split, symbols_strip,
                              symbols_to_lower, upper_list_if_true)


def test_symbols_map():
  result = symbols_map_outer(
    symbols=("a", "b", "c"),
    mapping={"a": "A", "b": "B"},
  )
  assert result == ("A", "B", "c")


def test_remove_space_around_punctuation__empty_input():
  result = remove_space_around_punctuation(
    symbols=(),
    space={},
    punctuation={},
  )

  assert result == ()


def test_remove_space_around_punctuation__before_and_after_space():
  result = remove_space_around_punctuation(
    symbols=("a", " ", ".", " ", "b"),
    space={" "},
    punctuation={"."},
  )

  assert result == ("a", ".", "b")


def test_remove_space_around_punctuation__multiple_punctuation_is_considered():
  result = remove_space_around_punctuation(
    symbols=("a", ".", " ", "b", "?", " ", "!", "c"),
    space={" "},
    punctuation={".", "?", "!"},
  )

  assert result == ("a", ".", "b", "?", "!", "c")


def test_remove_space_around_punctuation__multiple_space_is_considered():
  result = remove_space_around_punctuation(
    symbols=("a", " ", ".", "\t", "b"),
    space={" ", "\t"},
    punctuation={"."},
  )

  assert result == ("a", ".", "b")


def test_remove_space_around_punctuation__removes_only_one_space():
  result = remove_space_around_punctuation(
    symbols=("a", " ", " ", ".", " ", " ", "b"),
    space={" "},
    punctuation={"."},
  )

  assert result == ("a", " ", ".", " ", "b")


def test_split_symbols_on__separates_inside_split():
  result = split_symbols_on(
    symbols=("aa", "a-b", "bb",),
    split_symbols={"-"},
  )

  assert result == ("aa", "a", "b", "bb",)


def test_split_symbols_on__ignores_standalone_split_symbols():
  result = split_symbols_on(
    symbols=("aa", "-", "bb",),
    split_symbols={"-"},
  )

  assert result == ("aa", "bb",)


def test_split_symbols_on__empty_input():
  result = split_symbols_on(
    symbols=(),
    split_symbols={"-"},
  )

  assert result == ()


def test_split_symbols_on__split_on_right():
  result = split_symbols_on(
    symbols=("aa", "a-", "bb",),
    split_symbols={"-"},
  )

  assert result == ("aa", "a", "bb",)


def test_split_symbols_on__split_on_left():
  result = split_symbols_on(
    symbols=("aa", "-a", "bb",),
    split_symbols={"-"},
  )

  assert result == ("aa", "a", "bb",)


def test_split_symbols_on__separates_escapes_char():
  result = split_symbols_on(
    symbols=("aa", "a?b", "bb",),
    split_symbols={"?"},
  )

  assert result == ("aa", "a", "b", "bb",)


def test_sentence_to_words__empty_list():
  sentence = []

  res = symbols_split(sentence, split_symbols={" "})

  assert res == []


def test_sentence_to_words__only_one_space():
  sentence = (" ")

  res = symbols_split(sentence, split_symbols={" "})

  assert res == [(), ()]


def test_sentence_to_words__one_word():
  sentence = ("a")

  res = symbols_split(sentence, split_symbols={" "})

  assert res == [("a",)]


def test_sentence_to_words__two_words():
  sentence = ("a", " ", "b",)

  res = symbols_split(sentence, split_symbols={" "})

  assert res == [("a",), ("b",)]


def test_sentence_to_words__split_on_end():
  sentence = ("a", " ")

  res = symbols_split(sentence, split_symbols={" "})

  assert res == [("a",), ()]


def test_sentence_to_words__split_on_start():
  sentence = (" ", "a")

  res = symbols_split(sentence, split_symbols={" "})

  assert res == [(), ("a",)]


def test_sentence_to_words__multiple_split_symbols():
  sentence = ("a", ".", "b", "?", "c")

  res = symbols_split(sentence, split_symbols={".", "?"})

  assert res == [("a",), ("b",), ("c",)]


def test_symbols_separate__with_separate_at_end():
  sentence = ("a", ".", " ", "b", ".")
  res = symbols_separate(sentence, separate_symbols={"."})
  assert res == [("a", ".",), (" ", "b", "."), ()]


def test_remove_empty_symbols_list():
  res = remove_empty_symbols_list(["", "a", "", "b", ""])
  assert res == ["a", "b"]


def test_remove_empty_symbols():
  res = remove_empty_symbols(("", "a", "", "b", ""))
  assert res == ("a", "b")


def test_symbols_separate__without_separate_at_end():
  sentence = ("a", ".", " ", "b", "c")
  res = symbols_separate(sentence, separate_symbols={"."})
  assert res == [("a", ".",), (" ", "b", "c")]



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
