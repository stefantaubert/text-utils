import re
from logging import Logger
from typing import List

from dragonmapper import hanzi

from text_utils.ipa2symb import (ipa_of_phonetic_transcription,
                                 is_phonetic_transcription)
from text_utils.utils import split_text

CHN_SENTENCE_SEPARATORS = [r"？", r"！", r"。"]

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


def split_chn_text(text: str) -> List[str]:
  return split_text(text, CHN_SENTENCE_SEPARATORS)


def split_chn_sentence(sentence: str) -> List[str]:
  chn_words = sentence.split(" ")
  return chn_words


def chn_to_ipa(chn: str, logger: Logger) -> str:
  res_str = chn_sentence_to_ipa(chn, logger)
  for regex, replacement in CHN_SUBS:
    res_str = re.sub(regex, replacement, res_str)

  return res_str


def chn_word_to_ipa(word: str, logger: Logger) -> str:
  if is_phonetic_transcription(word):
    return ipa_of_phonetic_transcription(word, logger)
  return chn_ipa_of_word_not_containing_phonetic_transcription(word)


def chn_sentence_to_ipa(sentence: str, logger: Logger) -> str:
  chn_words = split_chn_sentence(sentence)
  res = [chn_word_to_ipa(word, logger) for word in chn_words]
  res_str = ' '.join(res)
  return res_str


def chn_ipa_of_word_not_containing_phonetic_transcription(word: str) -> str:
  assert not is_phonetic_transcription(word)
  chn_ipa = hanzi.to_ipa(word)
  chn_ipa = chn_ipa.replace(' ', '')
  return chn_ipa
