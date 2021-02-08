import logging
import time
import unittest
from logging import getLogger

from cmudict_parser import clear_cache

from text_utils.text import *


class UnitTests(unittest.TestCase):

  # region is_phonetic_transcription

  def test_is_phonetic_transcription__missing_space__returns_false(self):
    text = "/I/if"
    res = is_phonetic_transcription(text)

    self.assertFalse(res)

  # endregion

  # region en_to_ipa

  def test_en_to_ipa_with_phones(self):
    text = "This is /ð/ a test."
    res = en_to_ipa(text, EngToIpaMode.EPITRAN,
                    replace_unknown_with=None, use_cache=False, logger=getLogger())
    self.assertEqual("ðɪs ɪz ð ə tɛst.", res)

  def test_en_to_ipa_with_phones_at_beginning(self):
    text = "/ð/ a test."
    res = en_to_ipa(text, EngToIpaMode.EPITRAN,
                    replace_unknown_with=None, use_cache=False, logger=getLogger())
    self.assertEqual("ð ə tɛst.", res)

  def test_en_to_ipa_with_phones_at_end(self):
    text = "This is /ð/"
    res = en_to_ipa(text, EngToIpaMode.EPITRAN,
                    replace_unknown_with=None, use_cache=False, logger=getLogger())
    self.assertEqual("ðɪs ɪz ð", res)

  def test_en_to_ipa_with_only_phones(self):
    text = "/ð/"
    res = en_to_ipa(text, EngToIpaMode.EPITRAN,
                    replace_unknown_with=None, use_cache=False, logger=getLogger())
    self.assertEqual("ð", res)

  def test_en_to_ipa_with_only_phones_and_dot(self):
    text = "/ð./"
    res = en_to_ipa(text, EngToIpaMode.EPITRAN,
                    replace_unknown_with=None, use_cache=False, logger=getLogger())
    self.assertEqual("ð.", res)

  # endregion

  # region ger_to_ipa

  def test_ger_to_ipa_with_phones_logging_is_disabled(self):
    text = "Das ist /ð/ ein Test."
    getLogger().setLevel(0)
    ger_to_ipa(text, logger=getLogger())
    level = getLogger().level
    self.assertEqual(0, level)

  def test_ger_to_ipa_with_phones(self):
    text = "Das ist /ð/ ein Test."
    res = ger_to_ipa(text, logger=getLogger())
    self.assertEqual("das ist ð ain test.", res)

  def test_ger_to_ipa_with_phones_at_beginning(self):
    text = "/ð/ ein Test."
    res = ger_to_ipa(text, logger=getLogger())
    self.assertEqual("ð ain test.", res)

  def test_ger_to_ipa_with_phones_at_end(self):
    text = "Das ist /ð/"
    res = ger_to_ipa(text, logger=getLogger())
    self.assertEqual("das ist ð", res)

  def test_ger_to_ipa_with_only_phones(self):
    text = "/ð/"
    res = ger_to_ipa(text, logger=getLogger())
    self.assertEqual("ð", res)

  def test_ger_to_ipa_with_only_phones_and_dot(self):
    text = "/ð./"
    res = ger_to_ipa(text, logger=getLogger())
    self.assertEqual("ð.", res)

  # endregion

  # region chn_to_ipa

  def test_chn_to_ipa_with_phones(self):
    text = "东北军 的 一些 爱 /ð/ 东北军 的 一些 爱"
    res = chn_to_ipa(text, logger=getLogger())
    self.assertEqual("tʊŋ˥peɪ˧˩˧tɕyn˥ tɤ i˥ɕjɛ˥ aɪ˥˩ ð tʊŋ˥peɪ˧˩˧tɕyn˥ tɤ i˥ɕjɛ˥ aɪ˥˩", res)

  def test_chn_to_ipa_with_phones_at_beginning(self):
    text = "/ð/ 东北军 的 一些 爱"
    res = chn_to_ipa(text, logger=getLogger())
    self.assertEqual("ð tʊŋ˥peɪ˧˩˧tɕyn˥ tɤ i˥ɕjɛ˥ aɪ˥˩", res)

  def test_chn_to_ipa_with_phones_at_end(self):
    text = "东北军 的 一些 爱 /ð/"
    res = chn_to_ipa(text, logger=getLogger())
    self.assertEqual("tʊŋ˥peɪ˧˩˧tɕyn˥ tɤ i˥ɕjɛ˥ aɪ˥˩ ð", res)

  def test_chn_to_ipa_with_only_phones(self):
    text = "/ð/"
    res = chn_to_ipa(text, logger=getLogger())
    self.assertEqual("ð", res)

  def test_chn_to_ipa_with_only_phones_and_dot(self):
    text = "/ð./"
    res = chn_to_ipa(text, logger=getLogger())
    self.assertEqual("ð.", res)

  def test_normal(self):
    inp = "东北军 的 一些 爱"

    res = chn_to_ipa(inp, logger=getLogger())

    self.assertEqual('tʊŋ˥peɪ˧˩˧tɕyn˥ tɤ i˥ɕjɛ˥ aɪ˥˩', res)

  def test_chn_to_ipa(self):
    text = "。？！，：；「」『』、"

    res = chn_to_ipa(text, logger=getLogger())

    self.assertEqual('.?!,:;"""",', res)

  # endregion

  def test_text_to_symbols__no_settings_for_ipa__raise_exception(self):
    with self.assertRaises(ValueError):
      text_to_symbols(
        text="test",
        lang=Language.IPA,
        ipa_settings=None,
        logger=getLogger()
      )

  def test_text_to_ipa__no_mode_for_eng__raise_exception(self):
    with self.assertRaises(ValueError):
      text_to_ipa(
        text="test",
        lang=Language.ENG,
        mode=None,
        replace_unknown_with="_",
        use_cache=False,
        logger=getLogger(),
      )

  def test_en_to_ipa__no_replace_on_cmu__raise_exception(self):
    with self.assertRaises(ValueError):
      en_to_ipa(
        text="test",
        mode=EngToIpaMode.CMUDICT,
        replace_unknown_with=None,
        use_cache=False,
        logger=getLogger(),
      )

  def test_normalize_en(self):
    inp = "ü Hello my name is mr. test and    1 + 3 is $4. g 5e12  "
    res = normalize_en(inp)
    self.assertEqual(
      "u Hello my name is mister test and one + three is four dollars. grams five times ten to the power of twelve", res)

  def test_en_to_ipa__both_without_cache__takes_longer_time(self):
    # xyzxyz doesn't exist in CMUDict
    text = "xyzxyz"

    ensure_cmudict_is_loaded(getLogger())
    ensure_eng_epitran_is_loaded(getLogger())
    clear_cache()

    start = time.time()
    # , to prevent caching in cmudict, i could also clear the cache on every iteration
    res = [en_to_ipa(text + ("," * i), EngToIpaMode.BOTH,
                     replace_unknown_with="_", use_cache=False, logger=getLogger()) for i in range(100)]
    duration_s = time.time() - start

    self.assertTrue(duration_s < 9)
    self.assertEqual(100, len(res))
    self.assertEqual("zɪzksajz", res[0])

  def test_en_to_ipa__both_without_cache__takes_shorter_time(self):
    # xyzxyz doesn't exist in CMUDict
    text = "xyzxyz"

    ensure_cmudict_is_loaded(getLogger())
    ensure_eng_epitran_is_loaded(getLogger())
    clear_cache()
    clear_en_word_cache()

    start = time.time()
    # , to prevent caching in cmudict, i could also clear the cache on every iteration
    res = [en_to_ipa(text + ("," * i), EngToIpaMode.BOTH,
                     replace_unknown_with="_", use_cache=True, logger=getLogger()) for i in range(100)]
    duration_s = time.time() - start

    self.assertTrue(duration_s < 5)
    self.assertEqual(100, len(res))
    self.assertEqual("zɪzksajz", res[0])

  def test_en_to_ipa(self):
    text = "This is a test. And an other one."
    ensure_eng_epitran_is_loaded(getLogger())

    start = time.time()
    res = [en_to_ipa(text, EngToIpaMode.EPITRAN,
                     replace_unknown_with=None, use_cache=False, logger=getLogger()) for _ in range(25)]
    duration_s = time.time() - start

    # 21s with no caching
    # don't run training in parallel!
    self.assertTrue(duration_s < 6)
    self.assertEqual(25, len(res))
    self.assertEqual("ðɪs ɪz ə tɛst. ænd æn ʌðɹ̩ wʌn.", res[0])

  def test_ger_to_ipa(self):
    text = "Das ist ein Test. Und ein weiterer."
    ensure_ger_epitran_is_loaded(getLogger())

    start = time.time()
    res = [ger_to_ipa(text, getLogger()) for _ in range(25)]
    duration_s = time.time() - start
    # 16.39s with no caching
    self.assertTrue(duration_s < 2)
    self.assertEqual(25, len(res))
    self.assertEqual("das ist ain test. und ain vaieteːrər.", res[0])

  def test_split_chn_text(self):
    example_text = "This is a test。 And an other one。\nAnd a new line。\r\nAnd a line with \r。\n\nAnd a line with \n in it。 This is a question？ This is a error！"

    res = split_chn_text(example_text)

    self.assertEqual(7, len(res))
    self.assertEqual("This is a test。", res[0])
    self.assertEqual("And an other one。", res[1])
    self.assertEqual("And a new line。", res[2])
    self.assertEqual("And a line with \r。", res[3])
    self.assertEqual("And a line with \n in it。", res[4])
    self.assertEqual("This is a question？", res[5])
    self.assertEqual("This is a error！", res[6])

  def test_split_ipa(self):
    example_text = "This is a test. And an other one.\nAnd a new line.\r\nAnd a line with \r.\n\nAnd a line with \n in it. This is a question? This is a error!"
    res = split_ipa_text(example_text)
    self.assertEqual(7, len(res))
    self.assertEqual("This is a test.", res[0])
    self.assertEqual("And an other one.", res[1])
    self.assertEqual("And a new line.", res[2])
    self.assertEqual("And a line with \r.", res[3])
    self.assertEqual("And a line with \n in it.", res[4])
    self.assertEqual("This is a question?", res[5])
    self.assertEqual("This is a error!", res[6])

  def test_split_en(self):
    example_text = "This is a test 4.000. And an other one.\nAnd a new line.\r\nAnd a line with \r.\n\nAnd a line with \n in it. This is a question? This is a error!"
    res = split_en_text(example_text)
    self.assertEqual(7, len(res))
    self.assertEqual("This is a test 4.000.", res[0])
    self.assertEqual("And an other one.", res[1])
    self.assertEqual("And a new line.", res[2])
    self.assertEqual("And a line with \r.", res[3])
    self.assertEqual("And a line with \n in it.", res[4])
    self.assertEqual("This is a question?", res[5])
    self.assertEqual("This is a error!", res[6])

  def test_split_en_north(self):
    # Maybe include splitting on \n
    example_text = "his cloak around him;\nand at last."
    res = split_en_text(example_text)
    self.assertEqual(1, len(res))
    self.assertEqual("his cloak around him;\nand at last.", res[0])

  def test_split_ger(self):
    example_text = "Das ist ein Test 4.000. Und ein weiterer.\nUnd eine neue Zeile.\r\nUnd eine Zeile mit \r.\n\nUnd eine Zeile mit \n drin. Das ist eine Frage? Das ist ein Fehler!"
    res = split_ger_text(example_text)
    self.assertEqual(7, len(res))
    self.assertEqual("Das ist ein Test 4.000.", res[0])
    self.assertEqual("Und ein weiterer.", res[1])
    self.assertEqual("Und eine neue Zeile.", res[2])
    self.assertEqual("Und eine Zeile mit \r.", res[3])
    self.assertEqual("Und eine Zeile mit \n drin.", res[4])
    self.assertEqual("Das ist eine Frage?", res[5])
    self.assertEqual("Das ist ein Fehler!", res[6])

  # def test_period(self
  #   inp = "东北军 的 一些 爱"

  #   res = chn_to_ipa(inp)

  #   self.assertEqual('tʊŋ˥peɪ˧˩˧tɕyn˥ tɤ i˥ɕjɛ˥ aɪ˥˩。', res)

  # def test_question_mark_1(self):
  #   inp = "爱吗"

  #   res = chn_to_ipa(inp)

  #   self.assertEqual('aɪ˥˩ma？', res)

  # def test_question_mark_2(self):
  #   inp = "爱呢"

  #   res = chn_to_ipa(inp)

  #   self.assertEqual('aɪ˥˩nɤ？', res)

  # def test_line(self):
  #   inp = "东 一些"

  #   res = chn_to_ipa(inp)

  #   self.assertEqual('aɪ˥˩nɤ？', res)


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
