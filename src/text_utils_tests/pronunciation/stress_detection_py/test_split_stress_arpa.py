import string

from text_utils.pronunciation.arpa_symbols import CONSONANTS, VOWELS
from text_utils.pronunciation.stress_detection import (StressType,
                                                       split_stress_arpa)


def test_empty__returns_empty_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_arpa("")
  assert res_symbol == ""
  assert stress_type == StressType.NOT_APPLICABLE


def test_consonant_K__returns_K_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_arpa("K")
  assert res_symbol == "K"
  assert stress_type == StressType.NOT_APPLICABLE


def test_vowel_AA__returns_AA_UNSTRESSED():
  res_symbol, stress_type = split_stress_arpa("AA")
  assert res_symbol == "AA"
  assert stress_type == StressType.UNSTRESSED


def test_vowel_AA0__returns_AA_UNSTRESSED():
  res_symbol, stress_type = split_stress_arpa("AA0")
  assert res_symbol == "AA"
  assert stress_type == StressType.UNSTRESSED


def test_vowel_AA1__returns_AA_PRIMARY():
  res_symbol, stress_type = split_stress_arpa("AA1")
  assert res_symbol == "AA"
  assert stress_type == StressType.PRIMARY


def test_vowel_AA2__returns_AA_SECONDARY():
  res_symbol, stress_type = split_stress_arpa("AA2")
  assert res_symbol == "AA"
  assert stress_type == StressType.SECONDARY


def test_invalid_vowel_AA3__returns_AA3_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_arpa("AA3")
  assert res_symbol == "AA3"
  assert stress_type == StressType.NOT_APPLICABLE


def test_invalid_consonant_K0__returns_K0_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_arpa("K0")
  assert res_symbol == "K0"
  assert stress_type == StressType.NOT_APPLICABLE


def test_invalid_consonant_K1__returns_K1_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_arpa("K1")
  assert res_symbol == "K1"
  assert stress_type == StressType.NOT_APPLICABLE


def test_invalid_consonant_K2__returns_K2_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_arpa("K2")
  assert res_symbol == "K2"
  assert stress_type == StressType.NOT_APPLICABLE


def test_all_vowels_unstressed_no_nr__return_vowel_UNSTRESSED():
  for vowel in VOWELS:
    res_symbol, stress_type = split_stress_arpa(vowel)
    assert res_symbol == vowel
    assert stress_type == StressType.UNSTRESSED


def test_all_vowels_unstressed_0__return_vowel_UNSTRESSED():
  for vowel in VOWELS:
    res_symbol, stress_type = split_stress_arpa(vowel + "0")
    assert res_symbol == vowel
    assert stress_type == StressType.UNSTRESSED


def test_all_vowels_primary__return_vowel_PRIMARY():
  for vowel in VOWELS:
    res_symbol, stress_type = split_stress_arpa(vowel + "1")
    assert res_symbol == vowel
    assert stress_type == StressType.PRIMARY


def test_all_vowels_secondary__return_vowel_SECONDARY():
  for vowel in VOWELS:
    res_symbol, stress_type = split_stress_arpa(vowel + "2")
    assert res_symbol == vowel
    assert stress_type == StressType.SECONDARY


def test_all_consonants__return_consonant_NOT_APPLICABLE():
  for consonant in CONSONANTS:
    res_symbol, stress_type = split_stress_arpa(consonant)
    assert res_symbol == consonant
    assert stress_type == StressType.NOT_APPLICABLE


def test_punctuation__return_punctuation_NOT_APPLICABLE():
  res_symbol, stress_type = split_stress_arpa(".")
  assert res_symbol == "."
  assert stress_type == StressType.NOT_APPLICABLE


def test_special_characters__return_character_NOT_APPLICABLE():
  special_characters = set(string.punctuation) | set(string.whitespace)
  for character in special_characters:
    res_symbol, stress_type = split_stress_arpa(character)
    assert res_symbol == character
    assert stress_type == StressType.NOT_APPLICABLE
