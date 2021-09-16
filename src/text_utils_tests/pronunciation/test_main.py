
import pytest
from sentence2pronunciation import clear_cache
from text_utils.language import Language
from text_utils.pronunciation.main import (EngToIPAMode, __get_arpa_oov,
                                           __get_chn_ipa, __get_eng_ipa,
                                           __get_ger_ipa, chn_to_ipa,
                                           eng_to_arpa, eng_to_ipa,
                                           eng_to_ipa_epitran,
                                           eng_to_ipa_pronunciation_dict,
                                           ger_to_ipa, get_vowel_count,
                                           symbols_to_ipa)
from text_utils.symbol_format import SymbolFormat


def test_eng_to_arpa():
  result = eng_to_arpa(
    eng_sentence=tuple("This is a test."),
    consider_annotations=False,
  )

  clear_cache()
  assert result == ('DH', 'IH0', 'S', ' ', 'IH0', 'Z', ' ', 'AH0', ' ', 'T', 'EH1', 'S', 'T', ".",)


def test_get_arpa_oov():
  result = __get_arpa_oov(tuple("test"))

  clear_cache()
  assert result == ('T', 'EH1', 'S', 'T',)


def test_get_eng_ipa():
  result = __get_eng_ipa(tuple("test"))

  clear_cache()
  assert result == ('t', 'ɛ', 's', 't',)


def test__get_ger_ipa():
  result = __get_ger_ipa(tuple("test"))

  clear_cache()
  assert result == ('t', 'e', 's', 't',)


def test_eng_to_ipa_epitran():
  result = eng_to_ipa_epitran(
    eng_sentence=tuple("This is a test."),
    consider_annotations=False,
  )

  clear_cache()
  assert result == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ə', ' ', 't', 'ɛ', 's', 't', '.',)


def test_eng_to_ipa_epitran__with_annotations__is_considered():
  result = eng_to_ipa_epitran(
    eng_sentence=tuple("This /ɪz/ /ə/ə/ test."),
    consider_annotations=True,
  )

  clear_cache()
  assert result == ('ð', 'ɪ', 's', ' ', 'ɪz', ' ', 'ə', 'ə', ' ', 't', 'ɛ', 's', 't', '.',)


def test_eng_to_ipa_pronunciation_dict():
  result = eng_to_ipa_pronunciation_dict(
    eng_sentence=tuple("This is a test."),
    consider_annotations=False,
  )

  clear_cache()
  assert result == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ʌ', ' ', 't', 'ˈɛ', 's', 't', '.',)


def test_eng_to_ipa__epitran():
  result = eng_to_ipa(
    eng_sentence=tuple("This is a test."),
    consider_annotations=False,
    mode=EngToIPAMode.EPITRAN,
  )

  clear_cache()
  assert result == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ə', ' ', 't', 'ɛ', 's', 't', '.',)


def test_eng_to_ipa__librispeech():
  result = eng_to_ipa(
    eng_sentence=tuple("This is a test."),
    consider_annotations=False,
    mode=EngToIPAMode.LIBRISPEECH,
  )

  clear_cache()
  assert result == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ʌ', ' ', 't', 'ˈɛ', 's', 't', '.',)


def test_ger_to_ipa():
  result = ger_to_ipa(
    ger_sentence=tuple("This is a test."),
    consider_annotations=False,
  )

  clear_cache()
  assert result == ('t', 'i', 's', ' ', 'i', 's', ' ', 'a', ' ', 't', 'e', 's', 't', '.',)


def test_get_chn_ipa():
  result = __get_chn_ipa(tuple("堡包"))

  clear_cache()
  assert result == ('p', 'ɑʊ˧˩˧', 'p', 'ɑʊ˥',)


def test_get_chn_ipa__syllable_without_vowel():
  result = __get_chn_ipa(tuple("儿"))

  clear_cache()
  assert result == ('ɻ',)


def test_get_vowel_count__two():
  result = get_vowel_count(
    symbols=("a", "b", "aa",),
  )

  assert result == 2


def test_get_vowel_count__one_diphtong():
  result = get_vowel_count(
    symbols=("aa",),
  )

  assert result == 1


def test_get_vowel_count__one():
  result = get_vowel_count(
    symbols=("a",),
  )

  assert result == 1


def test_get_vowel_count__zero():
  result = get_vowel_count(
    symbols=(),
  )

  assert result == 0


def test_chn_to_ipa():
  result = chn_to_ipa(
    chn_sentence=tuple("石头 北 冷."),
    consider_annotations=False,
  )

  clear_cache()
  assert result == ('ʂ', 'ɨ˧˥', 'tʰ', 'oʊ', ' ', 'p', 'eɪ˧˩˧', ' ', 'l', 'ɤ˧˩˧', 'ŋ', '.',)


def test_chn_to_ipa__sentence():
  result = chn_to_ipa(
    chn_sentence=tuple("仅 绘画 而论 齐白石 是 巍巍 昆仑 可 这位 附庸风雅 的 门外汉 连 一块 石头 都 不是"),
    consider_annotations=False,
  )

  clear_cache()
  assert result == ('t', 'ɕ', 'i˧˩˧', 'n', ' ', 'x', 'w', 'eɪ˥˩', 'x', 'w', 'a˥˩', ' ', 'ɑ˧˥', 'ɻ', 'l', 'w', 'ə˥˩', 'n', ' ', 't', 'ɕʰ', 'i˧˥', 'p', 'aɪ˧˥', 'ʂ', 'ɨ˧˥', ' ', 'ʂ', 'ɨ˥˩', ' ', 'w', 'eɪ˥', 'w', 'eɪ˥', ' ', 'kʰ', 'w', 'ə˥', 'n', 'l', 'w', 'ə˧˥', 'n', ' ', 'kʰ', 'ɤ˧˩˧', ' ',
                    'ʈ', 'ʂ', 'ɤ˥˩', 'w', 'eɪ˥˩', ' ', 'f', 'u˥˩', 'yʊ˥', 'ŋ', 'f', 'ɤ˥', 'ŋ', 'j', 'a˧˩˧', ' ', 't', 'ɤ', ' ', 'm', 'ə˧˥', 'n', 'w', 'aɪ˥˩', 'x', 'a˥˩', 'n', ' ', 'l', 'j', 'ɛ˧˥', 'n', ' ', 'i˥', 'kʰ', 'w', 'aɪ˥˩', ' ', 'ʂ', 'ɨ˧˥', 'tʰ', 'oʊ', ' ', 't', 'oʊ˥', ' ', 'p', 'u˥˩', 'ʂ', 'ɨ˥˩')


def test_symbols_to_ipa__convert_arpa__raises_exception():
  with pytest.raises(Exception):
    symbols_to_ipa(
      symbols=tuple("This is a test."),
      consider_ipa_annotations=None,
      lang=Language.ENG,
      mode=EngToIPAMode.EPITRAN,
      symbols_format=SymbolFormat.PHONEMES_ARPA,
    )


def test_symbols_to_ipa__eng_no_mode__raises_exception():
  with pytest.raises(Exception):
    symbols_to_ipa(
      symbols=tuple("This is a test."),
      consider_ipa_annotations=False,
      lang=Language.ENG,
      mode=None,
      symbols_format=SymbolFormat.GRAPHEMES,
    )


def test_symbols_to_ipa__none_consider_annotation_on_graphemes__raises_exception():
  with pytest.raises(Exception):
    symbols_to_ipa(
      symbols=tuple("This is a test."),
      consider_ipa_annotations=None,
      lang=Language.ENG,
      mode=EngToIPAMode.EPITRAN,
      symbols_format=SymbolFormat.GRAPHEMES,
    )


def test_symbols_to_ipa__convert_english_graphemes():
  result_symbols, result_format = symbols_to_ipa(
    symbols=tuple("This is a test."),
    consider_ipa_annotations=False,
    lang=Language.ENG,
    mode=EngToIPAMode.EPITRAN,
    symbols_format=SymbolFormat.GRAPHEMES,
  )

  clear_cache()
  assert result_symbols == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ə', ' ', 't', 'ɛ', 's', 't', '.',)
  assert result_format == SymbolFormat.PHONEMES_IPA


def test_symbols_to_ipa__convert_ipa__returns_ipa():
  result_symbols, result_format = symbols_to_ipa(
    symbols=('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ə', ' ', 't', 'ɛ', 's', 't', '.',),
    consider_ipa_annotations=False,
    lang=Language.ENG,
    mode=None,
    symbols_format=SymbolFormat.PHONES_IPA,
  )

  clear_cache()
  assert result_symbols == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ə', ' ', 't', 'ɛ', 's', 't', '.',)
  assert result_format == SymbolFormat.PHONES_IPA

# def test_merge_symbols__no_merge_symbols():
#   res = merge_symbols(
#     pronunciation=("a", " ", "b",),
#     merge_at=" ",
#     merge_symbols={},
#   )

#   assert res == ("a", " ", "b",)


# def test_merge_symbols__empty_pron():
#   res = merge_symbols(
#     pronunciation=tuple(),
#     merge_at=" ",
#     merge_symbols={},
#   )

#   assert res == tuple()


# def test_merge_symbols__no_merge_at__only_merge_symbols__merges():
#   res = merge_symbols(
#     pronunciation=("?", "!"),
#     merge_at=" ",
#     merge_symbols={"?", "!"},
#   )

#   assert res == ("?!",)


# def test_merge_symbols__no_merge_at__merges():
#   res = merge_symbols(
#     pronunciation=("?", "b", "!"),
#     merge_at=" ",
#     merge_symbols={"?", "!"},
#   )

#   assert res == ("?b!",)


# def test_merge_symbols__merge_to_previous_symbol():
#   res = merge_symbols(
#     pronunciation=("a", " ", "b", "!"),
#     merge_at=" ",
#     merge_symbols={"!"},
#   )

#   assert res == ("a", " ", "b!",)


# def test_merge_symbols__dont_merge_if_no_symbol_to_merge():
#   res = merge_symbols(
#     pronunciation=("a", " ", "!",),
#     merge_at=" ",
#     merge_symbols={"!"},
#   )

#   assert res == ("a", " ", "!",)
