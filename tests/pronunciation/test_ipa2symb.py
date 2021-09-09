import re
import string

from text_utils.pronunciation.ipa2symb import (get_merge_group, get_next_symbol_for_merge_together,
                                               iterable_to_string, merge_left,
                                               merge_right, merge_together)

# region merge_together


def test_merge_together():
  res = merge_together(tuple("a&b&c&d&"), merge_symbols={"&"}, ignore_merge_symbols={"a"})
  assert res == ("a", "&", "b&c&d", "&",)

# endregion

# region iterable_to_string


def test_iterable_to_string():
  input_list = ["a", "bc", "def", 1]
  res = iterable_to_string(input_list)

  assert res == "abcdef1"

# endregion


# region get_merge_group


def test_get_merge_group_using_string_punctuation():
  merge_symbols = set(string.punctuation[:16])
  ignore_merge_symbols = set(string.punctuation[16:])
  res = get_merge_group(merge_symbols, ignore_merge_symbols)

  assert res.match("a" + string.punctuation[:16] + "b" + string.punctuation[:16] + "c")


def test_get_merge_group_using_string_punctuation_2():
  merge_symbols = set(string.punctuation[:16])
  ignore_merge_symbols = set(string.punctuation[16:])
  res = get_merge_group(merge_symbols, ignore_merge_symbols)

  assert res.match(string.punctuation[16] + string.punctuation[:16] +
                   "b" + string.punctuation[:16] + "c") is None


def test_get_merge_group_using_string_punctuation_3():
  merge_symbols = set(string.punctuation[:16])
  ignore_merge_symbols = set(string.punctuation[16:])
  res = get_merge_group(merge_symbols, ignore_merge_symbols)

  assert res.search(string.punctuation[16] +
                    string.punctuation[:16] + "b" + string.punctuation[:16] + "c")

# endregion


# region get_next_symbol_for_merge_together


def test_get_next_symbol_for_merge_together__get_group():
  symbols = "a&b&&cd"
  merge_group = get_merge_group({"&"}, {" "})
  res = get_next_symbol_for_merge_together(symbols, merge_group)

  assert res == "a&b&&c"

def test_get_next_symbol_for_merge_together__get_single_char():
  symbols = "a&b&&cd"
  merge_group = get_merge_group({"&"}, {" "})
  res = get_next_symbol_for_merge_together(symbols, merge_group)

  assert res == "a&b&&c"

# endregion

def test_merge_left():
  res = merge_left(tuple("'a,' b"), merge_symbols={"'"}, ignore_merge_symbols={" "})
  assert res == ("'a", ",", "'", " ", "b",)


def test_merge_left_abc():
  res = merge_left((",", "abc"), merge_symbols={","}, ignore_merge_symbols={" "})
  assert res == (",abc",)


def test_merge_right():
  res = merge_right(tuple("'a, ,'b!"), merge_symbols={"'", "!", ","}, ignore_merge_symbols={" "})
  assert res == ("'", "a,", " ", ",", "'", "b!",)


def test_merge_right_abc():
  res = merge_right(("abc", ","), merge_symbols={","}, ignore_merge_symbols={" "})
  assert res == ("abc,",)

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
