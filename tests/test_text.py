import time
from logging import getLogger

import pytest
from cmudict_parser import clear_cache
from text_utils.text import *
from text_utils.text import (delete_and_insert_in_list, is_sublist,
                             symbols_replace, upper_list_if_true)

# region is_phonetic_transcription


def test_is_phonetic_transcription__missing_space__returns_false():
  text = "/I/if"
  res = is_phonetic_transcription(text)

  assert not res

# endregion


def test_text_to_symbols_empty_input():
  res = text_to_symbols(
    text="",
    lang=Language.ENG,
    ipa_settings=None,
    logger=getLogger(__name__),
    merge_stress=None,
  )
  assert res == []

# region en_to_ipa


def test_en_to_ipa_with_phones():
  text = "This is /ð/ a test."
  res = en_to_ipa(text, EngToIpaMode.EPITRAN,
                  replace_unknown_with=None, use_cache=False, consider_ipa_annotations=True, logger=getLogger())
  assert res == "ðɪs ɪz ð ə tɛst."


def test_en_to_ipa_with_phones_at_beginning():
  text = "/ð/ a test."
  res = en_to_ipa(text, EngToIpaMode.EPITRAN,
                  replace_unknown_with=None, use_cache=False, consider_ipa_annotations=True, logger=getLogger())
  assert res == "ð ə tɛst."


def test_en_to_ipa_with_phones_at_end():
  text = "This is /ð/"
  res = en_to_ipa(text, EngToIpaMode.EPITRAN,
                  replace_unknown_with=None, use_cache=False, consider_ipa_annotations=True, logger=getLogger())
  assert res == "ðɪs ɪz ð"


def test_en_to_ipa_with_only_phones():
  text = "/ð/"
  res = en_to_ipa(text, EngToIpaMode.EPITRAN,
                  replace_unknown_with=None, use_cache=False, consider_ipa_annotations=True, logger=getLogger())
  assert res == "ð"


def test_en_to_ipa_with_only_phones_and_dot():
  text = "/ð./"
  res = en_to_ipa(text, EngToIpaMode.EPITRAN,
                  replace_unknown_with=None, use_cache=False, consider_ipa_annotations=True, logger=getLogger())
  assert res == "ð."

# endregion

# region ger_to_ipa


def test_ger_to_ipa_with_phones_logging_is_disabled():
  text = "Das ist /ð/ ein Test."
  getLogger().setLevel(0)
  ger_to_ipa(text, consider_ipa_annotations=True, logger=getLogger())
  level = getLogger().level
  assert level == 0


def test_ger_to_ipa_with_phones():
  text = "Das ist /ð/ ein Test."
  res = ger_to_ipa(text, consider_ipa_annotations=True, logger=getLogger())
  assert res == "das ist ð ain test."


def test_ger_to_ipa_with_phones_at_beginning():
  text = "/ð/ ein Test."
  res = ger_to_ipa(text, consider_ipa_annotations=True, logger=getLogger())
  assert res == "ð ain test."


def test_ger_to_ipa_with_phones_at_end():
  text = "Das ist /ð/"
  res = ger_to_ipa(text, consider_ipa_annotations=True, logger=getLogger())
  assert res == "das ist ð"


def test_ger_to_ipa_with_only_phones():
  text = "/ð/"
  res = ger_to_ipa(text, consider_ipa_annotations=True, logger=getLogger())
  assert res == "ð"


def test_ger_to_ipa_with_only_phones_and_dot():
  text = "/ð./"
  res = ger_to_ipa(text, consider_ipa_annotations=True, logger=getLogger())
  assert res == "ð."

# endregion

# region chn_to_ipa


def test_chn_to_ipa_with_phones():
  text = "东北军 的 一些 爱 /ð/ 东北军 的 一些 爱"
  res = chn_to_ipa(text, logger=getLogger())
  assert res == "tʊŋ˥peɪ˧˩˧tɕyn˥ tɤ i˥ɕjɛ˥ aɪ˥˩ ð tʊŋ˥peɪ˧˩˧tɕyn˥ tɤ i˥ɕjɛ˥ aɪ˥˩"


def test_chn_to_ipa_with_phones_at_beginning():
  text = "/ð/ 东北军 的 一些 爱"
  res = chn_to_ipa(text, logger=getLogger())
  assert res == "ð tʊŋ˥peɪ˧˩˧tɕyn˥ tɤ i˥ɕjɛ˥ aɪ˥˩"


def test_chn_to_ipa_with_phones_at_end():
  text = "东北军 的 一些 爱 /ð/"
  res = chn_to_ipa(text, logger=getLogger())
  assert res == "tʊŋ˥peɪ˧˩˧tɕyn˥ tɤ i˥ɕjɛ˥ aɪ˥˩ ð"


def test_chn_to_ipa_with_only_phones():
  text = "/ð/"
  res = chn_to_ipa(text, logger=getLogger())
  assert res == "ð"


def test_chn_to_ipa_with_only_phones_and_dot():
  text = "/ð./"
  res = chn_to_ipa(text, logger=getLogger())
  assert res == "ð."


def test_normal():
  inp = "东北军 的 一些 爱"

  res = chn_to_ipa(inp, logger=getLogger())

  assert res == 'tʊŋ˥peɪ˧˩˧tɕyn˥ tɤ i˥ɕjɛ˥ aɪ˥˩'


def test_chn_to_ipa():
  text = "。？！，：；「」『』、"

  res = chn_to_ipa(text, logger=getLogger())

  assert res == '.?!,:;"""",'

# endregion


def test_text_to_symbols__no_settings_for_ipa__raise_exception():
  with pytest.raises(ValueError):
    text_to_symbols(
      text="test",
      lang=Language.IPA,
      ipa_settings=None,
      logger=getLogger(),
      merge_stress=None,
    )


def test_text_to_ipa__no_mode_for_eng__raise_exception():
  with pytest.raises(ValueError):
    text_to_ipa(
      text="test",
      lang=Language.ENG,
      mode=None,
      replace_unknown_with="_",
      use_cache=False,
      consider_ipa_annotations=False,
      logger=getLogger(),
    )


def test_en_to_ipa__no_replace_on_cmu__raise_exception():
  with pytest.raises(ValueError):
    en_to_ipa(
      text="test",
      mode=EngToIpaMode.CMUDICT,
      replace_unknown_with=None,
      use_cache=False,
      consider_ipa_annotations=False,
      logger=getLogger(),
    )


def test_normalize_en():
  inp = "ü Hello my name is mr. test and    1 + 3 is $4. g 5e12  "
  res = normalize_en_grapheme_text(inp)
  assert res == "u Hello my name is mister test and one + three is four dollars. grams five times ten to the power of twelve"


def test_en_to_ipa__both_without_cache__takes_longer_time():
  # xyzxyz doesn't exist in CMUDict
  text = "xyzxyz"

  ensure_cmudict_is_loaded(getLogger())
  ensure_eng_epitran_is_loaded(getLogger())
  clear_cache()

  start = time.time()
  # , to prevent caching in cmudict, i could also clear the cache on every iteration
  res = [en_to_ipa(text + ("," * i), EngToIpaMode.BOTH,
                   replace_unknown_with="_", use_cache=False, consider_ipa_annotations=False, logger=getLogger()) for i in range(100)]
  duration_s = time.time() - start

  assert duration_s < 9
  assert len(res) == 100
  assert res[0] == "zɪzksajz"


def test_en_to_ipa__both_with_cache__takes_shorter_time():
  # xyzxyz doesn't exist in CMUDict
  text = "xyzxyz"

  ensure_cmudict_is_loaded(getLogger())
  ensure_eng_epitran_is_loaded(getLogger())
  clear_cache()
  clear_en_word_cache()

  start = time.time()
  # , to prevent caching in cmudict, i could also clear the cache on every iteration
  res = [en_to_ipa(text + ("," * i), EngToIpaMode.BOTH,
                   replace_unknown_with="_", use_cache=True, consider_ipa_annotations=False, logger=getLogger()) for i in range(100)]
  duration_s = time.time() - start

  assert duration_s < 5
  assert len(res) == 100
  assert res[0] == "zɪzksajz"


def test_en_to_ipa__epitran_with_cache__takes_shorter_time():
  # xyzxyz doesn't exist in CMUDict
  text = "xyzxyz"

  ensure_eng_epitran_is_loaded(getLogger())
  clear_cache()
  clear_en_word_cache()

  start = time.time()
  # , to prevent caching in cmudict, i could also clear the cache on every iteration
  res_cache = [en_to_ipa_epitran(text, logger=getLogger()) for i in range(100)]
  duration_cache = time.time() - start

  clear_cache()
  clear_en_word_cache()

  start = time.time()
  # , to prevent caching in cmudict, i could also clear the cache on every iteration
  _ = [en_to_ipa_epitran(
    text, logger=getLogger(), use_cache=False) for i in range(100)]
  duration_no_cache = time.time() - start

  assert duration_cache < duration_no_cache
  assert len(res_cache) == 100
  assert res_cache[0] == "zɪzksajz"


def test_en_to_ipa():
  text = "This is a test. And an other one."
  ensure_eng_epitran_is_loaded(getLogger())

  start = time.time()
  res = [en_to_ipa(text, EngToIpaMode.EPITRAN,
                   replace_unknown_with=None, use_cache=False, consider_ipa_annotations=False, logger=getLogger()) for _ in range(25)]
  duration_s = time.time() - start

  # 21s with no caching
  # don't run training in parallel!
  assert duration_s < 6
  assert len(res) == 25
  assert res[0] == "ðɪs ɪz ə tɛst. ænd æn ʌðɹ̩ wʌn."


def test_ger_to_ipa():
  text = "Das ist ein Test. Und ein weiterer."
  ensure_ger_epitran_is_loaded(getLogger())

  start = time.time()
  res = [ger_to_ipa(text, consider_ipa_annotations=False, logger=getLogger()) for _ in range(25)]
  duration_s = time.time() - start
  # 16.39s with no caching
  assert duration_s < 2
  assert len(res) == 25
  assert res[0] == "das ist ain test. und ain vaieteːrər."


def test_split_chn_text():
  example_text = "This is a test。 And an other one。\nAnd a new line。\r\nAnd a line with \r。\n\nAnd a line with \n in it。 This is a question？ This is a error！"

  res = split_chn_graphemes_text(example_text)

  assert len(res) == 7
  assert res[0] == "This is a test。"
  assert res[1] == "And an other one。"
  assert res[2] == "And a new line。"
  assert res[3] == "And a line with \r。"
  assert res[4] == "And a line with \n in it。"
  assert res[5] == "This is a question？"
  assert res[6] == "This is a error！"


def test_split_ipa():
  example_text = "This is a test. And an other one.\nAnd a new line.\r\nAnd a line with \r.\n\nAnd a line with \n in it. This is a question? This is a error!"
  res = split_ipa_text(example_text)
  assert len(res) == 7
  assert res[0] == "This is a test."
  assert res[1] == "And an other one."
  assert res[2] == "And a new line."
  assert res[3] == "And a line with \r."
  assert res[4] == "And a line with \n in it."
  assert res[5] == "This is a question?"
  assert res[6] == "This is a error!"


def test_split_en():
  example_text = "This is a test 4.000. And an other one.\nAnd a new line.\r\nAnd a line with \r.\n\nAnd a line with \n in it. This is a question? This is a error!"
  res = split_en_graphemes_text(example_text)
  assert len(res) == 7
  assert res[0] == "This is a test 4.000."
  assert res[1] == "And an other one."
  assert res[2] == "And a new line."
  assert res[3] == "And a line with \r."
  assert res[4] == "And a line with \n in it."
  assert res[5] == "This is a question?"
  assert res[6] == "This is a error!"


def test_split_en_north():
  # Maybe include splitting on \n
  example_text = "his cloak around him;\nand at last."
  res = split_en_graphemes_text(example_text)
  assert len(res) == 1
  assert res[0] == "his cloak around him;\nand at last."


def test_split_ger():
  example_text = "Das ist ein Test 4.000. Und ein weiterer.\nUnd eine neue Zeile.\r\nUnd eine Zeile mit \r.\n\nUnd eine Zeile mit \n drin. Das ist eine Frage? Das ist ein Fehler!"
  res = split_ger_graphemes_text(example_text)
  assert len(res) == 7
  assert res[0] == "Das ist ein Test 4.000."
  assert res[1] == "Und ein weiterer."
  assert res[2] == "Und eine neue Zeile."
  assert res[3] == "Und eine Zeile mit \r."
  assert res[4] == "Und eine Zeile mit \n drin."
  assert res[5] == "Das ist eine Frage?"
  assert res[6] == "Das ist ein Fehler!"

# def test_period(self
#   inp = "东北军 的 一些 爱"

#   res = chn_to_ipa(inp)

#   self.assertEqual('tʊŋ˥peɪ˧˩˧tɕyn˥ tɤ i˥ɕjɛ˥ aɪ˥˩。', res)

# def test_question_mark_1():
#   inp = "爱吗"

#   res = chn_to_ipa(inp)

#   self.assertEqual('aɪ˥˩ma？', res)

# def test_question_mark_2():
#   inp = "爱呢"

#   res = chn_to_ipa(inp)

#   self.assertEqual('aɪ˥˩nɤ？', res)

# def test_line():
#   inp = "东 一些"

#   res = chn_to_ipa(inp)

#   self.assertEqual('aɪ˥˩nɤ？', res)


def test_sentence_to_words__empty_list():
  sentence = []

  res = split_symbols(sentence)

  assert res == []


def test_sentence_to_words__only_one_space():
  sentence = [" "]

  res = split_symbols(sentence)

  assert res == [[], []]


def test_sentence_to_words__one_word():
  sentence = ["a"]

  res = split_symbols(sentence)

  assert res == [["a"]]


def test_sentence_to_words__two_words():
  sentence = ["a", " ", "b"]

  res = split_symbols(sentence)

  assert res == [["a"], ["b"]]


def test_words_to_sentence__empty_list():
  words = []

  res = symbols_join(words)

  assert res == []


def test_words_to_sentence__one_word():
  words = [["a"]]

  res = symbols_join(words)

  assert res == ["a"]


def test_words_to_sentence__two_words():
  words = [["a"], ["b"]]

  res = symbols_join(words)

  assert res == ["a", " ", "b"]


def test_strip_word__empty_word():
  word = []

  res = strip_symbols(word, ["a"])
  assert res == []


def test_strip_word__empty_strip():
  word = ["a"]

  res = strip_symbols(word, [])

  assert res == ["a"]


def test_strip_word__strip_start():
  word = ["a", "b"]

  res = strip_symbols(word, ["a"])

  assert res == ["b"]


def test_strip_word__strip_end():
  word = ["a", "b"]

  res = strip_symbols(word, ["b"])

  assert res == ["a"]


def test_strip_word__strip_start_and_end():
  word = ["b", "a", "b"]

  res = strip_symbols(word, ["b"])

  assert res == ["a"]


def test_strip_word__strip_start_and_end_multiple_symbols():
  word = ["b", "c", "a", "e", "b", "d"]

  res = strip_symbols(word, ["b", "c", "d"])

  assert res == ["a", "e"]


def test_strip_word__strip_not_inside():
  word = ["a", "b", "a"]

  res = strip_symbols(word, ["b"])

  assert res == ["a", "b", "a"]


def test_symbols_to_lower():
  res = symbols_to_lower(["A", "a", "B"])
  assert res == ["a", "a", "b"]


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
  symbols = ["abc", "def", "hij", "klm"]
  search_for = ["def", "hij"]
  replace_with = ["123"]
  res = symbols_replace(symbols, search_for, replace_with, True)

  assert res == ["abc", "123", "klm"]


def test_symbols_replace__two_occurences():
  symbols = ["abc", "def", "hij", "klm", "def", "hij"]
  search_for = ["def", "hij"]
  replace_with = ["123"]
  res = symbols_replace(symbols, search_for, replace_with, True)

  assert res == ["abc", "123", "klm", "123"]


def test_symbols_replace__no_occurence():
  symbols = ["abc", "def", "hij", "klm"]
  search_for = ["deF", "hij"]
  replace_with = ["123"]
  res = symbols_replace(symbols, search_for, replace_with, False)

  assert res == ["abc", "def", "hij", "klm"]


def test_symbols_replace__replace_whole_list():
  symbols = ["abc", "def", "hij", "klm"]
  search_for = ["abc", "def", "hij", "klm"]
  replace_with = ["abcdefg", "hijklmnop"]
  res = symbols_replace(symbols, search_for, replace_with, False)

  assert res == replace_with

# endregion
