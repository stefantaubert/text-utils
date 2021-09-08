
import pytest
from text_utils.language import Language
from text_utils.pronunciation.main import (EngToIPAMode, __get_arpa_oov,
                                           __get_chn_ipa, __get_eng_ipa,
                                           __get_ger_ipa, chn_to_ipa,
                                           eng_to_arpa, eng_to_ipa,
                                           eng_to_ipa_epitran,
                                           eng_to_ipa_pronunciation_dict,
                                           ger_to_ipa, symbols_to_ipa)
from text_utils.symbol_format import SymbolFormat


def test_eng_to_arpa():
  result = eng_to_arpa(
    eng_sentence="This is a test.",
    consider_annotations=False,
  )
  assert result == ('DH', 'IH0', 'S', ' ', 'IH0', 'Z', ' ', 'AH0', ' ', 'T', 'EH1', 'S', 'T', ".",)


def test_get_arpa_oov():
  result = __get_arpa_oov("test")
  assert result == ('T', 'EH1', 'S', 'T',)


def test_get_eng_ipa():
  result = __get_eng_ipa("test")
  assert result == ('t', 'ɛ', 's', 't',)


def test__get_ger_ipa():
  result = __get_ger_ipa("test")
  assert result == ('t', 'e', 's', 't',)


def test_eng_to_ipa_epitran():
  result = eng_to_ipa_epitran(
    eng_sentence="This is a test.",
    consider_annotations=False,
  )
  assert result == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ə', ' ', 't', 'ɛ', 's', 't', '.',)


def test_eng_to_ipa_epitran__with_annotations__is_considered():
  result = eng_to_ipa_epitran(
    eng_sentence="This /ɪz/ /ə/ə/ test.",
    consider_annotations=True,
  )
  assert result == ('ð', 'ɪ', 's', ' ', 'ɪz', ' ', 'ə', 'ə', ' ', 't', 'ɛ', 's', 't', '.',)


def test_eng_to_ipa_pronunciation_dict():
  result = eng_to_ipa_pronunciation_dict(
    eng_sentence="This is a test.",
    consider_annotations=False,
  )
  assert result == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ʌ', ' ', 't', 'ˈɛ', 's', 't', '.',)


def test_eng_to_ipa__epitran():
  result = eng_to_ipa(
    eng_sentence="This is a test.",
    consider_annotations=False,
    mode=EngToIPAMode.EPITRAN,
  )
  assert result == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ə', ' ', 't', 'ɛ', 's', 't', '.',)


def test_eng_to_ipa__librispeech():
  result = eng_to_ipa(
    eng_sentence="This is a test.",
    consider_annotations=False,
    mode=EngToIPAMode.LIBRISPEECH,
  )
  assert result == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ʌ', ' ', 't', 'ˈɛ', 's', 't', '.',)


def test_ger_to_ipa():
  result = ger_to_ipa(
    ger_sentence="This is a test.",
    consider_annotations=False,
  )
  assert result == ('t', 'i', 's', ' ', 'i', 's', ' ', 'a', ' ', 't', 'e', 's', 't', '.',)


def test_get_chn_ipa():
  result = __get_chn_ipa("堡包")
  assert result == ('p', 'ɑ', 'ʊ', '˧', '˩', '˧', ' ', 'p', 'ɑ', 'ʊ', '˥',)


def test_chn_to_ipa():
  result = chn_to_ipa(
    chn_sentence="北 冷.",
    consider_annotations=False,
  )
  assert result == ('p', 'e', 'ɪ', '˧', '˩', '˧', ' ', 'l', 'ɤ', 'ŋ', '˧', '˩', '˧', '.',)


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
