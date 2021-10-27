import pytest
from text_utils.language import Language
from text_utils.pronunciation.ipa2symb import (
    add_n_thongs, break_n_thongs, get_all_next_consecutive_merge_symbols,
    get_longest_possible_length, get_longest_template_with_ignore,
    get_next_merged_left_symbol_and_index,
    get_next_merged_right_symbol_and_index,
    get_next_merged_together_symbol_and_index, is_n_thong, merge_fusion,
    merge_left, merge_right, merge_template, merge_template_with_ignore,
    merge_together, remove_arcs, remove_ignore_at_end, split_string_to_tuple,
    try_update_longest_template)


def test_remove_arcs__empty_input():
  result = remove_arcs(
    symbols=(),
  )

  assert result == ()


def test_remove_arcs__component_tests():
  result = remove_arcs(
    symbols=("aa", "t͡ʃ", "t\u035Cʃ", "t", "\u0361", "ʃ", "t͡", "ʃ", "\u0361ʃ",),
  )

  assert result == ("aa", "t", "ʃ", "t", "ʃ", "t", "ʃ", "t", "ʃ", "ʃ",)


def test_add_n_thong__merges_eng_arpa_diphtong_ai():
  result = add_n_thongs(
    symbols=("b", "a", "ˈa", "ɪ\u031D", "a", "b"),
    language=Language.ENG,
  )

  assert result == ("b", "a", "ˈaɪ\u031D", "a", "b")


def test_is_n_thong__tripthong__is_true():
  result = is_n_thong("aaa")

  assert result


def test_is_n_thong__dipthong__is_true():
  result = is_n_thong("aa")

  assert result


def test_is_n_thong__dipthong_with_tones__is_true():
  result = is_n_thong("aa˦˦")

  assert result


def test_is_n_thong__double_consonant__is_false():
  result = is_n_thong("bb")

  assert not result


def test_is_n_thong__single_vowel__is_false():
  result = is_n_thong("a")

  assert not result


def test_is_n_thong__single_vowel_with_tone__is_false():
  result = is_n_thong("a˦")

  assert not result


def test_is_n_thong__single_consonant__is_false():
  result = is_n_thong("b")

  assert not result


def test_break_n_thongs__component_test():
  result = break_n_thongs(
    symbols=("aɪ˦˦", "b˦", "ˈaɪ", "˦a", "˦aɪ", "a\u0361ɪ"),
  )

  assert result == ("a", "ɪ˦˦", "b˦", "ˈa", "ɪ˦", "a˦", "a", "ɪ", "a\u0361ɪ")

# region split_string_to_tuple


def test_split_string_to_tuple():
  string_of_symbols = " abc   def "  # 3 Leerzeichen in Mitte
  split_symbol = " "
  res = split_string_to_tuple(string_of_symbols, split_symbol)

  assert res == ("abc", " ", "def")


def test_split_string_to_tuple2():
  string_of_symbols = "abc   def"  # 3 Leerzeichen in Mitte
  split_symbol = " "
  res = split_string_to_tuple(string_of_symbols, split_symbol)

  assert res == ("abc", " ", "def")


def test_split_string_to_tuple__two_split_symbols_in_middle():
  string_of_symbols = "abc  def"  # 2 Leerzeichen in Mitte
  split_symbol = " "
  res = split_string_to_tuple(string_of_symbols, split_symbol)

  assert res == ("abc", " def")


def test_split_string_to_tuple__four_split_symbols_in_middle():
  string_of_symbols = "abc    def"  # 4 Leerzeichen in Mitte
  split_symbol = " "
  res = split_string_to_tuple(string_of_symbols, split_symbol)

  assert res == ("abc", " ", " def")

# endregion

# region merge_template_with_ignore


def test_merge_template_with_ignore():
  symbols = ("ab:", "c", "d")
  template = {"abc"}
  ignore = {":"}
  res = merge_template_with_ignore(symbols, template, ignore)

  assert res == ("ab:c", "d")


def test_merge_template_with_ignore__ignore_symbol_is_also_part_of_template__raise_assertion_error():
  symbols = ("aba", "c", "d")
  template = {"abc", "def"}
  ignore = {"a", ":"}

  with pytest.raises(AssertionError):
    merge_template_with_ignore(symbols, template, ignore)


def test_merge_template_with_ignore__ignore_is_set_with_two_elements():
  symbols = ("ab:;", "c", "d")
  template = {"abc"}
  ignore = {":", ";"}
  res = merge_template_with_ignore(symbols, template, ignore)

  assert res == ("ab:;c", "d")


def test_merge_template_with_ignore__ignore_is_empty_set():
  symbols = ("ab:", "c", "d")
  template = {"abc"}
  ignore = {}
  res = merge_template_with_ignore(symbols, template, ignore)

  assert res == symbols


def test_merge_template_with_ignore__ignore_symbol_alone_in_middle():
  symbols = ("ab", ":", "c", "d")
  template = {"abc"}
  ignore = {":"}
  res = merge_template_with_ignore(symbols, template, ignore)

  assert res == ("ab:c", "d")


def test_merge_template_with_ignore__two_ignore_symbols_alone_in_middle():
  symbols = ("ab", ":", ":", "c", "d")
  template = {"abc"}
  ignore = {":"}
  res = merge_template_with_ignore(symbols, template, ignore)

  assert res == ("ab::c", "d")


def test_merge_template_with_ignore__ignore_symbol_at_beginning_of_one_tuple_entry_that_should_be_merged():
  symbols = (":ab", "c", "d")
  template = {"abc"}
  ignore = {":"}
  res = merge_template_with_ignore(symbols, template, ignore)

  assert res == (":abc", "d")


def test_merge_template_with_ignore__ignore_symbol_alone_at_beginning():
  symbols = (":", "ab", "c", "d")
  template = {"abc"}
  ignore = {":"}
  res = merge_template_with_ignore(symbols, template, ignore)

  assert res == (":", "abc", "d")


def test_merge_template_with_ignore__two_ignore_symbols_alone_at_beginning():
  symbols = (":", ":", "ab", "c", "d")
  template = {"abc"}
  ignore = {":"}
  res = merge_template_with_ignore(symbols, template, ignore)

  assert res == (":", ":", "abc", "d")


def test_merge_template_with_ignore__ignore_symbol_at_end_of_one_tuple_entry_that_should_be_merged():
  symbols = ("ab", "c:", "d")
  template = {"abc"}
  ignore = {":"}
  res = merge_template_with_ignore(symbols, template, ignore)

  assert res == ("abc:", "d")


def test_merge_template_with_ignore__ignore_symbol_alone_at_end_of_a_template():
  symbols = ("ab", "c", ":", "d")
  template = {"abc"}
  ignore = {":"}
  res = merge_template_with_ignore(symbols, template, ignore)

  assert res == ("abc", ":", "d")


def test_merge_template_with_ignore__two_ignore_symbols_alone_at_end_of_a_template():
  symbols = ("ab", "c", ":", ":", "d")
  template = {"abc"}
  ignore = {":"}
  res = merge_template_with_ignore(symbols, template, ignore)

  assert res == ("abc", ":", ":", "d")

# endregion

# region merge_template


def test_merge_region__should_merge_longest_in_template():
  symbols = ("a", "b", "c", "d")
  template = {"bc", "cd", "bcd"}
  res = merge_template(symbols, template)

  assert res == ("a", "bcd")


def test_merge_region__symbols_has_element_with_len_2__should_merge_longest_in_template():
  symbols = ("a", "bc", "d")
  template = {"bc", "cd", "bcd"}
  res = merge_template(symbols, template)

  assert res == ("a", "bcd")


def test_merge_region__symbols_has_element_with_len_2__no_template_fits():
  symbols = ("a", "bc", "d")
  template = {"cd"}
  res = merge_template(symbols, template)

  assert res == symbols


def test_merge_region__no_template_of_len_2():
  symbols = ("a", "b", "c", "d")
  template = {"bcd"}
  res = merge_template(symbols, template)

  assert res == ("a", "bcd")


def test_merge_region__should_merge_which_comes_first():
  symbols = ("a", "b", "c", "d")
  template = {"bc", "cd"}
  res = merge_template(symbols, template)

  assert res == ("a", "bc", "d")


def test_merge_region__symbols_is_empty_string():
  symbols = ("",)
  template = {"bc", "cd"}
  res = merge_template(symbols, template)

  assert res == ("",)


def test_merge_region__symbols_is_empty_tuple():
  symbols = ()
  template = {"bc", "cd"}
  res = merge_template(symbols, template)

  assert res == ()


def test_merge_region__template_is_empty_set():
  symbols = ("a", "b", "c", "d")
  template = {}
  res = merge_template(symbols, template)

  assert res == symbols


def test_merge_region__template_contains_only_empty_string():
  symbols = ("a", "b", "c", "d")
  template = {""}
  res = merge_template(symbols, template)

  assert res == symbols

# endregion

# region get_longest_template_with_ignore


def test_get_longest_template_with_ignore():
  symbols = ("a", "bc", "e")
  template = {"abc", "ab", "abcd"}
  ignore = {}
  res = get_longest_template_with_ignore(symbols, template, ignore)

  assert res == ("a", "bc")


def test_get_longest_template_with_ignore__three_ignore_symbols_in_middle_of_template():
  symbols = ("a", ":", ":", ":", "bc", "e")
  template = {"abc", "ab"}
  ignore = {":"}
  res = get_longest_template_with_ignore(symbols, template, ignore)

  assert res == ("a", ":", ":", ":", "bc")


def test_get_longest_template_with_ignore__one_ignore_symbol_at_beginning():
  symbols = (":", "bc", "e")
  template = {"bce"}
  ignore = {":"}
  res = get_longest_template_with_ignore(symbols, template, ignore)

  assert res == (":",)


def test_get_longest_template_with_ignore__two_ignore_symbols_at_beginning():
  symbols = (":", ":", "bc", "e")
  template = {"bce"}
  ignore = {":"}
  res = get_longest_template_with_ignore(symbols, template, ignore)

  assert res == (":",)


def test_get_longest_template_with_ignore__is_not_in_template():
  symbols = ("a", "c", "e")
  template = {"abc"}
  ignore = {}
  res = get_longest_template_with_ignore(symbols, template, ignore)

  assert res == ("a",)


def test_get_longest_template_with_ignore__longest_template_is_longer_than_symbols():
  symbols = ("a", "c", "e")
  template = {"abcdefg"}
  ignore = {}
  res = get_longest_template_with_ignore(symbols, template, ignore)

  assert res == ("a",)


def test_get_longest_template_with_ignore__template_is_empty():
  symbols = ("a",)
  template = {}
  ignore = {}
  res = get_longest_template_with_ignore(symbols, template, ignore)

  assert res == symbols

# endregion

# region get_longest_possible_length


def test_get_longest_possible_length():
  symbols = ("ab", ":", ":", ";", ":", "c")
  template = {"abc", "ab"}
  ignore = {":", ";"}
  res = get_longest_possible_length(symbols, template, ignore)

  assert res == 7

# endregion

# region try_update_longest_template


def test_try_update_longest_template__successful_updating():
  symbols = ("a", "c", "e")
  template = {"ac", "ace"}
  ignore = {":", ";"}
  res = try_update_longest_template(symbols, 2, template, ignore)

  assert res == ("a", "c")


def test_try_update_longest_template__successful_updating__in_middle_of_template_is_one_ignore_symbol():
  symbols = ("a:", "c", "e")
  template = {"ac", "ace"}
  ignore = {":", ";"}
  res = try_update_longest_template(symbols, 2, template, ignore)

  assert res == ("a:", "c")


def test_try_update_longest_template__successful_updating__in_middle_of_template_are_two_ignore_symbol():
  symbols = ("a:", ";c", "e")
  template = {"ac", "ace"}
  ignore = {":", ";"}
  res = try_update_longest_template(symbols, 2, template, ignore)

  assert res == ("a:", ";c")


def test_try_update_longest_template__successful_updating__ignore_is_empty():
  symbols = ("a", "c", "e")
  template = {"ac", "ace"}
  ignore = {}
  res = try_update_longest_template(symbols, 2, template, ignore)

  assert res == ("a", "c")


def test_try_update_longest_template__returns_none():
  symbols = ("a", "c", "e")
  template = {"ace"}
  ignore = {":", ";"}
  res = try_update_longest_template(symbols, 2, template, ignore)

  assert res is None

# endregion

# region remove_ignore_at_end


def test_remove_ignore_at_end__ignore_symbol_at_end_of_tuple_entry_but_not_alone_so_do_not_remove():
  template = ("abc:",)
  ignore = {":"}
  res = remove_ignore_at_end(template, ignore)

  assert res == template


def test_remove_ignore_at_end__ignore_symbol_at_end_of_tuple__remove():
  template = ("abc", ":")
  ignore = {":"}
  res = remove_ignore_at_end(template, ignore)

  assert res == ("abc",)


def test_remove_ignore_at_end__two_alone_ignore_symbol_at_end_of_tuple__remove_both():
  template = ("abc", ":", ";")
  ignore = {":", ";"}
  res = remove_ignore_at_end(template, ignore)

  assert res == ("abc",)

# endregion

# region merge_fusion


def test_merge_fusion():
  symbols = ("a", "b", "ef", "g")
  fusion_symbols = {"a", "b"}
  res = merge_fusion(symbols, fusion_symbols)

  assert res == ("ab", "ef", "g")


def test_merge_fusion_2():
  symbols = ("b", "ef", "a", "a", "g")
  fusion_symbols = {"a", "b"}
  res = merge_fusion(symbols, fusion_symbols)

  assert res == ("b", "ef", "aa", "g")

# endregion

# region merge_together


def test_merge_together():
  res = merge_together(tuple("a&b&c&d&"), merge_symbols={"&"}, ignore_merge_symbols={"a"})
  assert res == ("a", "&", "b&c&d", "&",)


def test_merge_together_double_and():
  res = merge_together(tuple("a&b&&c&d&"), merge_symbols={"&"}, ignore_merge_symbols={"a"})
  assert res == ("a", "&", "b&&c&d", "&",)

# endregion

# region get_next_merged_together_symbol_and_index


def test_get_next_merged_together_symbol_and_index__whole_symbols_merged_together():
  symbols = ("a", "&", "&", "b")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  res_1, res_2 = get_next_merged_together_symbol_and_index(
    symbols, 0, merge_symbols, merge_symbols.union(ignore_merge_symbols))

  assert res_1 == "a&&b"
  assert res_2 == 4


def test_get_next_merged_together_symbol_and_index__not_merged_together_because_of_ignore_merge_symbol_after_merge_symbol():
  symbols = ("a", "&", " ")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  res_1, res_2 = get_next_merged_together_symbol_and_index(
    symbols, 0, merge_symbols, merge_symbols.union(ignore_merge_symbols))

  assert res_1 == "a"
  assert res_2 == 1


def test_get_next_merged_together_symbol_and_index__not_merged_together_because_of_ignore_merge_symbol_for_merge_symbol():
  symbols = (" ", "&", "a")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  res_1, res_2 = get_next_merged_together_symbol_and_index(
    symbols, 0, merge_symbols, merge_symbols.union(ignore_merge_symbols))

  assert res_1 == " "
  assert res_2 == 1


def test_get_next_merged_together_symbol_and_index__not_merged_together_because_no_symbol_after_merge_symbols():
  symbols = ("a", "&", "&")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  res_1, res_2 = get_next_merged_together_symbol_and_index(
    symbols, 0, merge_symbols, merge_symbols.union(ignore_merge_symbols))

  assert res_1 == "a"
  assert res_2 == 1


def test_get_next_merged_together_symbol_and_index__consider_last_element():
  symbols = ("a", "&", "b")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  res_1, res_2 = get_next_merged_together_symbol_and_index(
    symbols, 2, merge_symbols, merge_symbols.union(ignore_merge_symbols))

  assert res_1 == "b"
  assert res_2 == 3

# endregion

# region get_all_next_consecutive_merge_symbols


def test_get_all_next_consecutive_merge_symbols__first_symbol_is_merge_symbol_second_is_not():
  symbols = ("&", "a")
  merge_symbols = {"&"}
  res_1, res_2 = get_all_next_consecutive_merge_symbols(symbols, merge_symbols)

  assert res_1 == "&"
  assert res_2 == 1


def test_get_all_next_consecutive_merge_symbols__first_symbol_is_not_merge_symbol():
  symbols = ("a", "&")
  merge_symbols = {"&"}
  res_1, res_2 = get_all_next_consecutive_merge_symbols(symbols, merge_symbols)

  assert res_1 == ""
  assert res_2 == 0


def test_get_all_next_consecutive_merge_symbols__first_and_second_symbols_are_merge_symbols_but_third_symbol_is_not():
  symbols = ("&", "&", "a")
  merge_symbols = {"&"}
  res_1, res_2 = get_all_next_consecutive_merge_symbols(symbols, merge_symbols)

  assert res_1 == "&&"
  assert res_2 == 2


def test_get_all_next_consecutive_merge_symbols__first_and_second_symbols_are_merge_symbols_third_symbol_does_not_exist():
  symbols = ("&", "&")
  merge_symbols = {"&"}
  res_1, res_2 = get_all_next_consecutive_merge_symbols(symbols, merge_symbols)

  assert res_1 == "&&"
  assert res_2 == 1

# endregion

# region merge_left


def test_merge_left():
  res = merge_left(tuple("'a,' b"), merge_symbols={
                   "'"}, ignore_merge_symbols={" "}, insert_symbol="?")
  assert res == ("'?a", ",", "'", " ", "b",)


def test_merge_left_abc():
  res = merge_left((",", "abc", ","), merge_symbols={
                   ","}, ignore_merge_symbols={" "}, insert_symbol="?")
  assert res == (",?abc", ",")


def test_merge_left__insert_symbol_is_None():
  res = merge_left(tuple("'a,' b"), merge_symbols={
                   "'"}, ignore_merge_symbols={" "}, insert_symbol=None)
  assert res == ("'a", ",", "'", " ", "b",)


def test_merge_left__insert_symbol_consists_of_two_chars():
  res = merge_left(tuple("'a,' b"), merge_symbols={
                   "'"}, ignore_merge_symbols={" "}, insert_symbol="?$")
  assert res == ("'?$a", ",", "'", " ", "b",)


def test_merge_left__merge_symbols_are_not_merged_if_no_non_ignore_symbol_exists():
  res = merge_left(" -- ", merge_symbols={"-"}, ignore_merge_symbols={" "}, insert_symbol=None)
  assert res == (" ", "-", "-", " ")


# endregion

# region merge_right


def test_merge_right():
  res = merge_right(tuple("'a, ,'b!"), merge_symbols={
                    "'", "!", ","}, ignore_merge_symbols={" "}, insert_symbol="?")
  assert res == ("'", "a?,", " ", ",", "'", "b?!",)


def test_merge_right_abc():
  res = merge_right((",", "abc", ","), merge_symbols={
                    ","}, ignore_merge_symbols={" "}, insert_symbol="?")
  assert res == (",", "abc?,",)


def test_merge_right__insert_symbol_is_None():
  res = merge_right(tuple("'a, ,'b!"), merge_symbols={
                    "'", "!", ","}, ignore_merge_symbols={" "}, insert_symbol=None)
  assert res == ("'", "a,", " ", ",", "'", "b!",)


def test_merge_right__insert_symbol_consists_of_two_chars():
  res = merge_right(tuple("'a, ,'b!"), merge_symbols={
                    "'", "!", ","}, ignore_merge_symbols={" "}, insert_symbol="?$")
  assert res == ("'", "a?$,", " ", ",", "'", "b?$!",)

# endregion

# region get_next_merged_left_symbol_and_index


def test_get_next_merged_left_symbol_and_index__from_left_is_true__index_is_zero__first_symbol_is_not_merge_or_ignore_merge_symbol_but_second_is_merge_symbol():
  symbols = ("a", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?"
  res_1, res_2 = get_next_merged_left_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "&?a"
  assert res_2 == 2


def test_get_next_merged_left_symbol_and_index__from_left_is_true__index_is_zero__first_symbol_is_not_merge_or_ignore_merge_symbol_but_second_is_merge_symbol__insert_symbols_is_empty():
  symbols = ("a", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = ""
  res_1, res_2 = get_next_merged_left_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "&a"
  assert res_2 == 2


def test_get_next_merged_left_symbol_and_index__from_left_is_true__index_is_zero__first_symbol_is_not_merge_or_ignore_merge_symbol_but_second_is_merge_symbol__insert_symbols_consists_of_two_chars():
  symbols = ("a", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?$"
  res_1, res_2 = get_next_merged_left_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "&?$a"
  assert res_2 == 2


def test_get_next_merged_left_symbol_and_index__from_left_is_true__index_is_zero__first_symbol_has_length_greater_than_1_and_is_not_merge_or_ignore_merge_symbol_but_second_is_merge_symbol():
  symbols = ("abc", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?"
  res_1, res_2 = get_next_merged_left_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "&?abc"
  assert res_2 == 2


def test_get_next_merged_left_symbol_and_index__from_left_is_true__index_is_zero__first_symbol_is_not_merge_or_ignore_merge_symbol_but_second_and_third_are_merge_symbols():
  symbols = ("a", "&", "&")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?"
  res_1, res_2 = get_next_merged_left_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "&?&?a"
  assert res_2 == 3


def test_get_next_merged_left_symbol_and_index__from_left_is_true__index_is_zero__first_symbol_is_not_merge_or_ignore_merge_symbol_second_is_ignore_merge_symbol():
  symbols = ("a", " ", "&")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?"
  res_1, res_2 = get_next_merged_left_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "a"
  assert res_2 == 1


def test_get_next_merged_left_symbol_and_index__from_left_is_true__index_is_zero__first_symbol_is_ignore_merge_symbol():
  symbols = (" ", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?"
  res_1, res_2 = get_next_merged_left_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == " "
  assert res_2 == 1


def test_get_next_merged_left_symbol_and_index__from_left_is_true__index_is_zero__first_symbol_is_merge_symbol_second_one_is_not():
  symbols = ("&", "a", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?"
  res_1, res_2 = get_next_merged_left_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "&"
  assert res_2 == 1


def test_get_next_merged_left_symbol_and_index__from_left_is_true__index_is_zero__first_symbol_is_merge_symbol_second_one_is_too():
  symbols = ("&", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?"
  res_1, res_2 = get_next_merged_left_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "&"
  assert res_2 == 1


def test_get_next_merged_left_symbol_and_index__from_left_is_true__index_is_last__last_symbol_is_not_merge_or_ignore_merge_symbol():
  symbols = ("a", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?"
  res_1, res_2 = get_next_merged_left_symbol_and_index(
    symbols, 2, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "bc"
  assert res_2 == 3


def test_get_next_merged_left_symbol_and_index__from_left_is_true__index_is_last__last_symbol_is_ignore_merge_symbol():
  symbols = ("a", "&", " ")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?"
  res_1, res_2 = get_next_merged_left_symbol_and_index(
    symbols, 2, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == " "
  assert res_2 == 3


def test_get_next_merged_left_symbol_and_index__from_left_is_true__index_is_last__first_symbol_is_merge_symbol_second_one_is_not():
  symbols = ("a", "bc", "&")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?"
  res_1, res_2 = get_next_merged_left_symbol_and_index(
    symbols, 2, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "&"
  assert res_2 == 3

# endregion

# region get_next_merged_right_symbol_and_index


def test_get_next_merged_right_symbol_and_index__from_left_is_false__index_is_zero__first_symbol_is_not_merge_or_ignore_merge_symbol_but_second_is_merge_symbol():
  symbols = ("a", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?"
  res_1, res_2 = get_next_merged_right_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "a?&"
  assert res_2 == 2


def test_get_next_merged_right_symbol_and_index__from_left_is_false__index_is_zero__first_symbol_is_not_merge_or_ignore_merge_symbol_but_second_is_merge_symbol__insert_symbol_is_empty():
  symbols = ("a", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = ""
  res_1, res_2 = get_next_merged_right_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "a&"
  assert res_2 == 2


def test_get_next_merged_right_symbol_and_index__from_left_is_false__index_is_zero__first_symbol_is_not_merge_or_ignore_merge_symbol_but_second_is_merge_symbol__insert_symbol_consists_of_two_chars():
  symbols = ("a", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?$"
  res_1, res_2 = get_next_merged_right_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "a?$&"
  assert res_2 == 2


def test_get_next_merged_right_symbol_and_index__from_left_is_false__index_is_zero__first_symbol_has_length_greater_than_1_and_is_not_merge_or_ignore_merge_symbol_but_second_is_merge_symbol():
  symbols = ("abc", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?"
  res_1, res_2 = get_next_merged_right_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "abc?&"
  assert res_2 == 2


def test_get_next_merged_right_symbol_and_index__from_left_is_false__index_is_zero__first_symbol_is_not_merge_or_ignore_merge_symbol_but_second_and_third_are_merge_symbols():
  symbols = ("a", "&", "&")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  insert_symbol = "?"
  res_1, res_2 = get_next_merged_right_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, insert_symbol)

  assert res_1 == "a?&?&"
  assert res_2 == 3

# endregion


# def test_unprocessable_ipa():
#   text = "ɡɹât͡ʃi"
#   settings = IPAExtractionSettings(
#     ignore_tones=True,
#     ignore_arcs=True,
#     replace_unknown_ipa_by='_'
#   )

#   res = extract_from_sentence(text, settings, getLogger())

#   assert res == ['_', '_', '_', '_', '_', '_', '_']


# def test_check_is_ipa_and_return_closest_ipa__pure_ipa():
#   text = "ʊʌʒθ"
#   res = check_is_ipa_and_return_closest_ipa(text)

#   assert len(res) == 2
#   assert res[0]
#   assert str(res[1]) == text


# def test_check_is_ipa_and_return_closest_ipa__ipa_with_letters():
#   text = "Hʊʌʒ-θ2"
#   res = check_is_ipa_and_return_closest_ipa(text)

#   assert len(res) == 2
#   assert not res[0]
#   assert str(res[1]) == "ʊʌʒθ"


# def test_check_is_ipa_and_return_closest_ipa__no_ipa():
#   text = "H-2"
#   res = check_is_ipa_and_return_closest_ipa(text)

#   assert len(res) == 2
#   assert not res[0]
#   assert str(res[1]) == ""


# def test_ipa_str_to_list__extracts_symbols():
#   ipa_str = IPAString(unicode_string="mntu", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=False, merge_stress=False)

#   assert result == ["m", "n", "t", "u"]


# def test_ipa_str_to_list__ignore_tones__ignores_tones():
#   ipa_str = IPAString(unicode_string="ɔ̄̋ɔ̄̏̄ɔ̋ɔ̋̏", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=True, ignore_arcs=False, merge_stress=False)

#   assert result == ["ɔ", "ɔ", "ɔ", "ɔ"]


# def test_ipa_str_to_list__ignore_arcs__ignores_arcs():
#   ipa_str = IPAString(unicode_string="t͡ʃ", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=True, merge_stress=False)

#   assert result == ["t", "ʃ"]


# def test_ipa_str_to_list__ignore_arcs_on_end__ignores_arcs():
#   ipa_str = IPAString(unicode_string="t͡", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=True, merge_stress=False)

#   assert result == ["t"]


# def test_ipa_str_to_list__merges_diacritics():
#   ipa_str = IPAString(unicode_string="t͡ʃpʰ", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=False, merge_stress=False)

#   assert result == ["t͡ʃ", "pʰ"]


# def test_ipa_str_to_list__merges_open_diacritics():
#   ipa_str = IPAString(unicode_string="t͡", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=False, merge_stress=False)

#   assert result == ["t͡"]


# def test_ipa_str_to_list__stress_is_own_symbol():
#   ipa_str = IPAString(unicode_string="ˌnˈt", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=False, merge_stress=False)

#   assert result == ["ˌ", "n", "ˈ", "t"]


# def test_ipa_str_to_list__merge_stress__merges_stress():
#   ipa_str = IPAString(unicode_string="ˌnˈt", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=False, merge_stress=True)

#   assert result == ["ˌn", "ˈt"]


# def test_ipa_str_to_list__merge_stress_before_arc__not_ignore_arc__merges_stress():
#   ipa_str = IPAString(unicode_string="ˌt͡ʃˈt͡ʃ", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=False, merge_stress=True)

#   assert result == ["ˌt͡ʃ", "ˈt͡ʃ"]


# def test_ipa_str_to_list__merge_stress_before_arc__ignore_arc__merges_stress():
#   ipa_str = IPAString(unicode_string="ˌt͡ʃˈt͡ʃ", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=True, merge_stress=True)

#   assert result == ["ˌt", "ʃ", "ˈt", "ʃ"]


# def test_ipa_str_to_list__merge_stress_before_arc__stress_after_arc__merges_stress():
#   ipa_str = IPAString(unicode_string="ˌt͡ˈʃ", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=False, merge_stress=True)

#   assert result == ["ˌt͡", "ˈʃ"]


# def test_ipa_str_to_list__dont_merge_stress_before_arc__stress_after_arc__dont_merges_stress():
#   ipa_str = IPAString(unicode_string="ˌt͡ˈʃ", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=False, merge_stress=False)

#   assert result == ["ˌ", "t͡", "ˈ", "ʃ"]


# def test_ipa_str_to_list__merge_stress__dont_merge_stress_on_end():
#   ipa_str = IPAString(unicode_string="ˌnˈ", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=False, merge_stress=True)

#   assert result == ["ˌn", "ˈ"]


# def test_ipa_str_to_list__merge_stress__double_stress():
#   ipa_str = IPAString(unicode_string="ˌˈ", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=False, merge_stress=True)

#   assert result == ["ˌˈ"]


# def test_ipa_str_to_list__dont_merge_stress__double_stress():
#   ipa_str = IPAString(unicode_string="ˌˈ", ignore=False)

#   result = ipa_str_to_list(ipa_str, ignore_tones=False, ignore_arcs=False, merge_stress=False)

#   assert result == ["ˌ", "ˈ"]
