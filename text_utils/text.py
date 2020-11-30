import re
from enum import IntEnum
from typing import Dict, List, Optional

from cmudict_parser import CMUDict, get_dict
from dragonmapper import hanzi
from epitran import Epitran
from nltk import download
from nltk.tokenize import sent_tokenize
from unidecode import unidecode as convert_to_ascii

from text_utils.adjustments.abbreviations import (
    expand_abbreviations, expand_units_of_measure,
    replace_big_letter_abbreviations)
from text_utils.adjustments.emails import (replace_at_symbols,
                                           replace_mail_addresses)
from text_utils.adjustments.numbers import normalize_numbers
from text_utils.adjustments.whitespace import collapse_whitespace
from text_utils.ipa2symb import extract_from_sentence
from text_utils.language import Language

EPITRAN_CACHE: Dict[Language, Epitran] = {}

CMU_CACHE: Optional[CMUDict] = None


class EngToIpaMode(IntEnum):
  EPITRAN = 0
  CMUDICT = 1
  BOTH = 2


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


def en_to_ipa(text: str, mode: EngToIpaMode) -> str:
  if mode is None:
    raise Exception("Assert")
  if mode == EngToIpaMode.EPITRAN:
    return en_to_ipa_epitran(text)
  if mode == EngToIpaMode.CMUDICT:
    return en_to_ipa_cmu(text)
  if mode == EngToIpaMode.BOTH:
    return en_to_ipa_cmu_epitran(text)
  raise Exception()


def en_to_ipa_epitran(text: str) -> str:
  global EPITRAN_CACHE
  if Language.ENG not in EPITRAN_CACHE.keys():
    EPITRAN_CACHE[Language.ENG] = Epitran('eng-Latn')
  result = EPITRAN_CACHE[Language.ENG].transliterate(text)
  return result


def en_to_ipa_cmu_epitran(text: str) -> str:
  global CMU_CACHE
  global EPITRAN_CACHE
  if CMU_CACHE is None:
    CMU_CACHE = get_dict(silent=True)
  if Language.ENG not in EPITRAN_CACHE.keys():
    EPITRAN_CACHE[Language.ENG] = Epitran('eng-Latn')
  result = CMU_CACHE.sentence_to_ipa(
    sentence=text,
    # replace_unknown_with=EPITRAN_CACHE[Language.ENG].transliterate
    replace_unknown_with=en_to_ipa_epi_verbose
  )
  return result


def en_to_ipa_epi_verbose(word: str) -> str:
  global EPITRAN_CACHE
  res = EPITRAN_CACHE[Language.ENG].transliterate(word)
  print(f"used Epitran for: {word} => {res}")
  return res


def en_to_ipa_cmu(text: str) -> str:
  global CMU_CACHE
  if CMU_CACHE is None:
    CMU_CACHE = get_dict(silent=True)
  result = CMU_CACHE.sentence_to_ipa(
    sentence=text,
    replace_unknown_with="_"
  )
  return result


def ger_to_ipa(text: str) -> str:
  global EPITRAN_CACHE
  if Language.GER not in EPITRAN_CACHE.keys():
    EPITRAN_CACHE[Language.GER] = Epitran('deu-Latn')
  result = EPITRAN_CACHE[Language.GER].transliterate(text)
  return result


def normalize_en(text: str) -> str:
  text = convert_to_ascii(text)
  # text = text.lower()
  # todo datetime conversion
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

  raise Exception()


def text_to_ipa(text: str, lang: Language, mode: Optional[EngToIpaMode]) -> str:
  if lang == Language.ENG:
    return en_to_ipa(text, mode)

  if lang == Language.GER:
    return ger_to_ipa(text)

  if lang == Language.CHN:
    return chn_to_ipa(text)

  if lang == Language.IPA:
    return text

  raise Exception()


def text_to_sentences(text: str, lang: Language) -> List[str]:
  if lang == Language.CHN:
    return split_chn_text(text)

  if lang == Language.IPA:
    return split_ipa_text(text)

  if lang == Language.ENG:
    return split_en_text(text)

  if lang == Language.GER:
    return split_ger_text(text)

  raise Exception()


def text_to_symbols(text: str, lang: Language, ignore_tones: Optional[bool] = None, ignore_arcs: Optional[bool] = None, padding_symbol: Optional[str] = None) -> List[str]:
  if lang == Language.ENG or lang == Language.GER or lang == Language.CHN:
    return list(text)
  if lang == Language.IPA:
    return extract_from_sentence(
      text,
      ignore_tones=ignore_tones,
      ignore_arcs=ignore_arcs,
      padding_symbol=padding_symbol,
    )

  raise Exception()


def split_text(text: str, separators: List[str]) -> List[str]:
  pattern = "|".join(separators)
  sents = re.split(f'({pattern})', text)
  res = []
  for i, sent in enumerate(sents):
    if i % 2 == 0:
      res.append(sent)
      if i + 1 < len(sents):
        res[-1] += sents[i + 1]
  res = [x.strip() for x in res]
  res = [x for x in res if x]
  return res


def split_en_text(text: str) -> List[str]:
  download('punkt', quiet=True)
  res = sent_tokenize(text, language="english")
  return res


def split_ger_text(text: str) -> List[str]:
  download('punkt', quiet=True)
  res = sent_tokenize(text, language="german")
  return res


def split_ipa_text(text: str) -> List[str]:
  separators = [r"\?", r"\!", r"\."]
  return split_text(text, separators)


def split_chn_text(text: str) -> List[str]:
  separators = [r"？", r"！", r"。"]
  return split_text(text, separators)


def split_chn_sentence(sentence: str) -> List[str]:
  chn_words = sentence.split(' ')
  return chn_words


def chn_to_ipa(chn: str):
  chn_words = split_chn_sentence(chn)
  res = []
  for word in chn_words:
    chn_ipa = hanzi.to_ipa(word)
    chn_ipa = chn_ipa.replace(' ', '')
    res.append(chn_ipa)
  res_str = ' '.join(res)

  for regex, replacement in CHN_SUBS:
    res_str = re.sub(regex, replacement, res_str)

  return res_str
