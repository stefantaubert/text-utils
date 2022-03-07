import string

from text_utils.pronunciation.ipa_symbols import (CONSONANTS, ENG_DIPHTHONGS,
                                                  SCHWAS, VOWELS)
from text_utils.pronunciation.stress_detection import (StressType,
                                                       split_stress_ipa)


def test_empty__returns_empty_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_ipa("")
  assert res_symbol == ""
  assert stress_type == StressType.NOT_APPLICABLE


def test_consonant_k__returns_k_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_ipa("k")
  assert res_symbol == "k"
  assert stress_type == StressType.NOT_APPLICABLE


def test_vowel_i__returns_i_UNSTRESSED():
  res_symbol, stress_type = split_stress_ipa("i")
  assert res_symbol == "i"
  assert stress_type == StressType.UNSTRESSED


def test_vowel_stressed_i__returns_i_PRIMARY():
  res_symbol, stress_type = split_stress_ipa("ˈi")
  assert res_symbol == "i"
  assert stress_type == StressType.PRIMARY


def test_vowel_secondary_stressed_i__returns_i_SECONDARY():
  res_symbol, stress_type = split_stress_ipa("ˌi")
  assert res_symbol == "i"
  assert stress_type == StressType.SECONDARY


def test_primary_stress__returns_stress_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_ipa("ˈ")
  assert res_symbol == "ˈ"
  assert stress_type == StressType.NOT_APPLICABLE


def test_secondary_stress__returns_stress_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_ipa("ˌ")
  assert res_symbol == "ˌ"
  assert stress_type == StressType.NOT_APPLICABLE


def test_invalid_primary_stressed_consonant_k__returns_k_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_ipa("ˈk")
  assert res_symbol == "ˈk"
  assert stress_type == StressType.NOT_APPLICABLE


def test_invalid_secondary_stressed_consonant_k__returns_k_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_ipa("ˌk")
  assert res_symbol == "ˌk"
  assert stress_type == StressType.NOT_APPLICABLE


def test_all_vowels_unstressed__return_vowel_UNSTRESSED():
  for vowel in VOWELS:
    res_symbol, stress_type = split_stress_ipa(vowel)
    assert res_symbol == vowel
    assert stress_type == StressType.UNSTRESSED


def test_all_vowels_primary_stressed__return_vowel_PRIMARY():
  for vowel in VOWELS:
    res_symbol, stress_type = split_stress_ipa("ˈ" + vowel)
    assert res_symbol == vowel
    assert stress_type == StressType.PRIMARY


def test_all_vowels_secondary_stressed__return_vowel_PRIMARY():
  for vowel in VOWELS:
    res_symbol, stress_type = split_stress_ipa("ˌ" + vowel)
    assert res_symbol == vowel
    assert stress_type == StressType.SECONDARY


def test_all_consonants__return_consonant_NOT_APPLICABLE():
  for consonant in CONSONANTS:
    res_symbol, stress_type = split_stress_ipa(consonant)
    assert res_symbol == consonant
    assert stress_type == StressType.NOT_APPLICABLE


def test_punctuation__return_punctuation_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_ipa(".")
  assert res_symbol == "."
  assert stress_type == StressType.NOT_APPLICABLE


def test_special_characters__return_character_NOT_APPLICABLE():
  special_characters = set(string.punctuation) | set(string.whitespace)
  for character in special_characters:
    res_symbol, stress_type = split_stress_ipa(character)
    assert res_symbol == character
    assert stress_type == StressType.NOT_APPLICABLE


def test_all_schwas_primary_stressed__return_schwa_PRIMARY():
  for schwa in SCHWAS:
    res_symbol, stress_type = split_stress_ipa("ˈ" + schwa)
    assert res_symbol == schwa
    assert stress_type == StressType.PRIMARY


def test_all_diphthongs_primary_stressed__return_diphthong_PRIMARY():
  for diphthong in ENG_DIPHTHONGS:
    res_symbol, stress_type = split_stress_ipa("ˈ" + diphthong)
    assert res_symbol == diphthong
    assert stress_type == StressType.PRIMARY


def test_appendix_is_stripped__unstressed_vowel_long_i__returns_long_i_UNSTRESSED():
  res_symbol, stress_type = split_stress_ipa("iː")
  assert res_symbol == "iː"
  assert stress_type == StressType.UNSTRESSED


def test_appendix_is_stripped__primary_stressed_vowel_long_i__returns_long_i_PRIMARY():
  res_symbol, stress_type = split_stress_ipa("ˈiː")
  assert res_symbol == "iː"
  assert stress_type == StressType.PRIMARY


def test_appendix_is_stripped__secondary_stressed_vowel_long_i__returns_long_i_SECONDARY():
  res_symbol, stress_type = split_stress_ipa("ˌiː")
  assert res_symbol == "iː"
  assert stress_type == StressType.SECONDARY


def test_double_stress_is_ignored__double_primary_stress_i__returns__unchanged_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_ipa("ˌˌi")
  assert res_symbol == "ˌˌi"
  assert stress_type == StressType.NOT_APPLICABLE


def test_double_stress_is_ignored__double_primary_stress_long_i__returns__unchanged_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_ipa("ˌˌiː")
  assert res_symbol == "ˌˌiː"
  assert stress_type == StressType.NOT_APPLICABLE


def test_double_vowel_ii__returns__unchanged_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_ipa("ii")
  assert res_symbol == "ii"
  assert stress_type == StressType.NOT_APPLICABLE
