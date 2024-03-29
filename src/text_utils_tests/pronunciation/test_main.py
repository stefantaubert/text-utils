
import pytest
from ordered_set import OrderedSet
from sentence2pronunciation.lookup_cache import get_empty_cache
from text_utils.language import Language
from text_utils.pronunciation.main import (EngToIPAMode, __get_arpa_oov,
                                           __get_eng_ipa, __get_ger_ipa,
                                           eng_to_arpa, eng_to_ipa,
                                           eng_to_ipa_epitran,
                                           eng_to_ipa_pronunciation_dict,
                                           ger_to_ipa, symbols_to_arpa,
                                           symbols_to_arpa_pronunciation_dict,
                                           symbols_to_ipa)
from text_utils.symbol_format import SymbolFormat
from text_utils.types import Symbol


def test_eng_to_arpa():
  result = eng_to_arpa(
    eng_sentence=tuple("This is a test."),
    consider_annotations=False,
    cache=get_empty_cache(),
  )

  assert result == ('DH', 'IH0', 'S', ' ', 'IH0', 'Z', ' ', 'AH0', ' ', 'T', 'EH1', 'S', 'T', ".",)


def test_get_arpa_oov():
  result = __get_arpa_oov(tuple("test"))

  assert result == ('T', 'EH1', 'S', 'T')


def test_get_eng_ipa():
  result = __get_eng_ipa(tuple("test"))

  assert result == ('t', 'ɛ', 's', 't')


def test_get_eng_ipa__ties_are_merged():
  result = __get_eng_ipa(tuple("Chinese"))

  assert result == ('t͡ʃ', 'a', 'j', 'n', 'i', 'z')


def test__get_ger_ipa():
  result = __get_ger_ipa(tuple("test"))

  assert result == ('t', 'e', 's', 't')


def test_eng_to_ipa_epitran():
  result = eng_to_ipa_epitran(
    eng_sentence=tuple("This is a test."),
    consider_annotations=False,
    cache=get_empty_cache(),
  )

  assert result == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ə', ' ', 't', 'ɛ', 's', 't', '.')


def test_eng_to_ipa_epitran__with_annotations__is_considered():
  result = eng_to_ipa_epitran(
    eng_sentence=tuple("This /ɪz/ /ə/ə/ test."),
    consider_annotations=True,
    cache=get_empty_cache(),
  )

  assert result == ('ð', 'ɪ', 's', ' ', 'ɪz', ' ', 'ə', 'ə', ' ', 't', 'ɛ', 's', 't', '.')


def test_eng_to_ipa_pronunciation_dict():
  result = eng_to_ipa_pronunciation_dict(
    eng_sentence=tuple("This is a test."),
    consider_annotations=False,
    cache=get_empty_cache(),
  )

  assert result == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ʌ', ' ', 't', 'ˈɛ', 's', 't', '.')


def test_eng_to_ipa_pronunciation_dict__dont_merge_diphtongs():
  result = eng_to_ipa_pronunciation_dict(
    eng_sentence=tuple("immediately"),
    consider_annotations=False,
    cache=get_empty_cache(),
  )

  assert result == ('ɪ', 'm', 'ˈi', 'd', 'i', 'ʌ', 't', 'l', 'i')


def test_eng_to_ipa__epitran():
  result = eng_to_ipa(
    eng_sentence=tuple("This is a test."),
    consider_annotations=False,
    mode=EngToIPAMode.EPITRAN,
    cache=get_empty_cache(),
  )

  assert result == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ə', ' ', 't', 'ɛ', 's', 't', '.')


def test_eng_to_ipa__librispeech():
  result = eng_to_ipa(
    eng_sentence=tuple("This is a test."),
    consider_annotations=False,
    mode=EngToIPAMode.LIBRISPEECH,
    cache=get_empty_cache(),
  )

  assert result == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ʌ', ' ', 't', 'ˈɛ', 's', 't', '.')


def test_ger_to_ipa():
  result = ger_to_ipa(
    ger_sentence=tuple("This is a test."),
    consider_annotations=False,
    cache=get_empty_cache(),
  )

  assert result == ('t', 'i', 's', ' ', 'i', 's', ' ', 'a', ' ', 't', 'e', 's', 't', '.')


def test_symbols_to_ipa__convert_arpa__raises_exception():
  with pytest.raises(Exception):
    symbols_to_ipa(
      symbols=tuple("This is a test."),
      consider_annotations=None,
      lang=Language.ENG,
      mode=EngToIPAMode.EPITRAN,
      symbols_format=SymbolFormat.PHONEMES_ARPA,
      cache=get_empty_cache(),
    )


def test_symbols_to_ipa__eng_no_mode__raises_exception():
  with pytest.raises(Exception):
    symbols_to_ipa(
      symbols=tuple("This is a test."),
      consider_annotations=False,
      lang=Language.ENG,
      mode=None,
      symbols_format=SymbolFormat.GRAPHEMES,
      cache=get_empty_cache(),
    )


def test_symbols_to_ipa__none_consider_annotation_on_graphemes__raises_exception():
  with pytest.raises(Exception):
    symbols_to_ipa(
      symbols=tuple("This is a test."),
      consider_annotations=None,
      lang=Language.ENG,
      mode=EngToIPAMode.EPITRAN,
      symbols_format=SymbolFormat.GRAPHEMES,
      cache=get_empty_cache(),
    )


def test_symbols_to_ipa__convert_english_graphemes():
  result_symbols, result_format = symbols_to_ipa(
    symbols=tuple("This is a test."),
    consider_annotations=False,
    lang=Language.ENG,
    mode=EngToIPAMode.EPITRAN,
    symbols_format=SymbolFormat.GRAPHEMES,
    cache=get_empty_cache(),
  )

  assert result_symbols == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ə', ' ', 't', 'ɛ', 's', 't', '.')
  assert result_format == SymbolFormat.PHONEMES_IPA


def test_symbols_to_ipa__convert_ipa__returns_ipa():
  result_symbols, result_format = symbols_to_ipa(
    symbols=('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ə', ' ', 't', 'ɛ', 's', 't', '.'),
    consider_annotations=False,
    lang=Language.ENG,
    mode=None,
    symbols_format=SymbolFormat.PHONES_IPA,
    cache=get_empty_cache(),
  )

  assert result_symbols == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ə', ' ', 't', 'ɛ', 's', 't', '.')
  assert result_format == SymbolFormat.PHONES_IPA


def test_symbols_to_arpa():
  result, result_format = symbols_to_arpa(
    symbols=tuple("This is a test /AA/BB/"),
    consider_annotations=True,
    lang=Language.ENG,
    symbols_format=SymbolFormat.GRAPHEMES,
    cache=get_empty_cache(),
  )

  assert result == ('DH', 'IH0', 'S', ' ', 'IH0', 'Z', ' ', 'AH0',
                    ' ', 'T', 'EH1', 'S', 'T', ' ', 'AA', 'BB')
  assert result_format == SymbolFormat.PHONEMES_ARPA


def test_symbols_to_pronunciation_dict():
  result = symbols_to_arpa_pronunciation_dict(
    symbols=tuple("This!, ?a .is-a test /bb/"),
    language=Language.ENG,
    symbols_format=SymbolFormat.GRAPHEMES,
    ignore_case=True,
    split_on_hyphen=True,
    consider_annotations=True,
    cache=get_empty_cache(),
  )

  assert len(result) == 4
  assert result["THIS"] == OrderedSet([('DH', 'IH0', 'S')])
  assert result["IS"] == OrderedSet([('IH0', 'Z')])
  assert result["A"] == OrderedSet([('AH0',)])
  assert result["TEST"] == OrderedSet([('T', 'EH1', 'S', 'T')])


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
