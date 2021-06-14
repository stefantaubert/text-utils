from logging import getLogger

from text_utils.ipa2symb import IPAExtractionSettings, extract_from_sentence
from text_utils.text import check_is_ipa_and_return_closest_ipa


def test_unprocessable_ipa():
  text = "ɡɹât͡ʃi"
  settings = IPAExtractionSettings(
    ignore_tones=True,
    ignore_arcs=True,
    replace_unknown_ipa_by='_'
  )

  res = extract_from_sentence(text, settings, getLogger())

  assert res == ['_', '_', '_', '_', '_', '_', '_']


def test_check_is_ipa_and_return_closest_ipa__pure_ipa():
  text = "ʊʌʒθ"
  res = check_is_ipa_and_return_closest_ipa(text)

  assert len(res) == 2
  assert res[0]
  assert str(res[1]) == text


def test_check_is_ipa_and_return_closest_ipa__ipa_with_letters():
  text = "Hʊʌʒ-θ2"
  res = check_is_ipa_and_return_closest_ipa(text)

  assert len(res) == 2
  assert not res[0]
  assert str(res[1]) == "ʊʌʒθ"


def test_check_is_ipa_and_return_closest_ipa__no_ipa():
  text = "H-2"
  res = check_is_ipa_and_return_closest_ipa(text)

  assert len(res) == 2
  assert not res[0]
  assert str(res[1]) == ""
