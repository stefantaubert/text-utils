import re
from typing import List

from nltk import download
from nltk.tokenize import sent_tokenize
from unidecode import unidecode as convert_to_ascii

from text_utils.adjustments import (collapse_whitespace, expand_abbreviations,
                                    expand_units_of_measure, normalize_numbers,
                                    replace_at_symbols,
                                    replace_big_letter_abbreviations,
                                    replace_mail_addresses)
from text_utils.language import Language
from text_utils.types import Symbols
from text_utils.utils import split_text

CHN_MAPPINGS = [
  (r"。", "."),
  (r"？", "?"),
  (r"！", "!"),
  (r"，", ","),
  (r"：", ":"),
  (r"；", ";"),
  (r"「", "\""),
  (r"」", "\""),
  (r"『", "\""),
  (r"』", "\""),
  (r"、", ",")
]

CHN_SUBS = [(re.compile(regex_pattern), replace_with)
            for regex_pattern, replace_with in CHN_MAPPINGS]
IPA_SENTENCE_SEPARATORS = [r"\?", r"\!", r"\."]


def split_ipa_text(text: str) -> List[str]:
  return split_text(text, IPA_SENTENCE_SEPARATORS)


def replace_chn_punctuation_with_default_punctuation(chn_sentence: str) -> str:
  for regex, replacement in CHN_SUBS:
    chn_sentence = re.sub(regex, replacement, chn_sentence)
  return chn_sentence



def normalize_en(text: str) -> str:
  text = convert_to_ascii(text)
  # text = text.lower()
  # TODO datetime conversion
  text = text.strip()
  text = normalize_numbers(text)
  text = expand_abbreviations(text)
  text = expand_units_of_measure(text)
  text = replace_big_letter_abbreviations(text)
  text = replace_mail_addresses(text)
  text = replace_at_symbols(text)
  text = collapse_whitespace(text)
  return text


def normalize_ger(text: str) -> str:
  text = text.strip()
  text = collapse_whitespace(text)
  return text


def normalize_ipa(text: str) -> str:
  return text.strip()


def normalize_chn(text: str) -> str:
  text = text.strip()
  text = collapse_whitespace(text)
  text = replace_chn_punctuation_with_default_punctuation(text)
  return text


def text_normalize(text: str, lang: Language) -> str:
  if lang == Language.ENG:
    return normalize_en(text)

  if lang == Language.GER:
    return normalize_ger(text)

  if lang == Language.CHN:
    return normalize_chn(text)

  if lang == Language.IPA:
    return normalize_ipa(text)

  assert False


def text_to_sentences(text: str, lang: Language) -> List[str]:
  if lang == Language.CHN:
    return split_chn_text(text)

  if lang == Language.IPA:
    return split_ipa_text(text)

  if lang == Language.ENG:
    return split_en_text(text)

  if lang == Language.GER:
    return split_ger_text(text)

  assert False


CHN_SENTENCE_SEPARATORS = [r"？", r"！", r"。"]


def split_chn_text(text: str) -> Symbols:
  return split_text(text, CHN_SENTENCE_SEPARATORS)


# def text_to_symbols(text: str, lang: Language, ipa_settings: Optional[IPAExtractionSettings], logger: Logger, merge_stress: Optional[bool] = True) -> Symbols:
#   if lang in (Language.ENG, Language.GER, Language.CHN):
#     return tuple(text)
#   if lang == Language.IPA:
#     if ipa_settings is None:
#       ex = ValueError(f"You have to pass ipa_settings for {lang!r}!")
#       logger.error("", exc_info=ex)
#       raise ex

#     return tuple(extract_from_sentence(
#       ipa_sentence=text,
#       settings=ipa_settings,
#       merge_stress=merge_stress,
#     ))

#   assert False


def split_en_text(text: str) -> List[str]:
  download('punkt', quiet=True)
  res = sent_tokenize(text, language="english")
  return res


def split_ger_text(text: str) -> List[str]:
  download('punkt', quiet=True)
  res = sent_tokenize(text, language="german")
  return res
