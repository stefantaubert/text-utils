import re
from enum import IntEnum
from functools import partial
from logging import WARNING, Logger, getLogger
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
from text_utils.ipa2symb import IPAExtractionSettings, extract_from_sentence
from text_utils.language import Language

EPITRAN_CACHE: Dict[Language, Epitran] = {}
EPITRAN_EN_WORD_CACHE: Dict[str, str] = {}

CMU_CACHE: Optional[CMUDict] = None

WHOLE_STRING_IS_PHONETIC_TRANS = re.compile(r'\A/\S*/\Z')
#WHOLE_STRING_IS_PHONETIC_TRANS = re.compile(r'/\S*/')
SLASH = re.compile(r'/')
PH_TRANS = re.compile(r'/(\S*)/')
#PH_TRANS = re.compile(r'([^ ]*)/(\S*)/([^ ]*)')


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


def en_to_ipa(text: str, mode: EngToIpaMode, replace_unknown_with: Optional[str], use_cache: bool, logger: Logger) -> str:
  assert mode is not None
  if is_phonetic_transcription_in_text(text):
    words = text.split(" ")
    ipa_list = [
      ipa_of_phonetic_transcription(word)
        if is_phonetic_transcription(word)
        else en_ipa_of_text_not_containing_phonetic_transcription(
        text=word,
        mode=mode,
        replace_unknown_with=replace_unknown_with,
        use_cache=use_cache,
        logger=logger
          )
        for word in words
    ]
    res = " ".join(ipa_list)
    return res
  return en_ipa_of_text_not_containing_phonetic_transcription(
     text=text,
     mode=mode,
     replace_unknown_with=replace_unknown_with,
     use_cache=use_cache,
     logger=logger
    )


def en_ipa_of_text_not_containing_phonetic_transcription(
    text: str,
    mode: EngToIpaMode,
    replace_unknown_with: Optional[str],
    use_cache: bool,
    logger: Logger
  ) -> str:
  if mode == EngToIpaMode.EPITRAN:
    return en_to_ipa_epitran(text, logger)
  if mode == EngToIpaMode.CMUDICT:
    if replace_unknown_with is None:
      ex = ValueError(f"Parameter replace_unknown_with is required for {mode!r}!")
      logger.error("", exc_info=ex)
      raise ex
    return en_to_ipa_cmu(text, replace_unknown_with, logger)
  if mode == EngToIpaMode.BOTH:
    return en_to_ipa_cmu_epitran(text, use_cache, logger)

  assert False


def is_phonetic_transcription_in_text(text: str) -> bool:
  #ph_trans_in_text = PH_TRANS_NO_WHITESPACE.match(text)
  ph_trans_in_text = PH_TRANS.search(text)
  return ph_trans_in_text is not None


def ipa_of_phonetic_transcription(ph_trans: str) -> str:
  assert is_phonetic_transcription(ph_trans)
  return re.sub(SLASH, '', ph_trans)


def is_phonetic_transcription(text: str) -> bool:
  ipa_of_ph_trans = WHOLE_STRING_IS_PHONETIC_TRANS.search(text)
  return ipa_of_ph_trans is not None


def en_to_ipa_epitran(text: str, logger: Logger) -> str:
  global EPITRAN_CACHE

  ensure_eng_epitran_is_loaded(logger)

  result = epi_transliterate_without_logging(EPITRAN_CACHE[Language.ENG], text)
  # result = EPITRAN_CACHE[Language.ENG].transliterate(text)
  return result


def ensure_eng_epitran_is_loaded(logger: Logger) -> None:
  global EPITRAN_CACHE
  if Language.ENG not in EPITRAN_CACHE.keys():
    logger.info("Loading English Epitran...")
    EPITRAN_CACHE[Language.ENG] = Epitran('eng-Latn')


def ensure_ger_epitran_is_loaded(logger: Logger) -> None:
  global EPITRAN_CACHE
  if Language.GER not in EPITRAN_CACHE.keys():
    logger.info("Loading German Epitran...")
    EPITRAN_CACHE[Language.GER] = Epitran('deu-Latn')


def ensure_cmudict_is_loaded(logger: Logger) -> None:
  global CMU_CACHE
  if CMU_CACHE is None:
    logger.info("Loading CMU dictionary...")
    CMU_CACHE = get_dict(silent=True)


def en_to_ipa_cmu_epitran(text: str, use_cache: bool, logger: Logger) -> str:
  global CMU_CACHE

  ensure_cmudict_is_loaded(logger)
  ensure_eng_epitran_is_loaded(logger)

  try:
    replacing_func = partial(epi_transliterate_word_cached, logger=logger) if use_cache else partial(
        epi_transliterate_word_verbose, logger=logger)

    result = CMU_CACHE.sentence_to_ipa(
      sentence=text,
      replace_unknown_with=replacing_func
    )
    return result
  except Exception as orig_exception:
    ex = ValueError(f"Conversion of '{text}' was not successfull!")
    logger.error("", exc_info=ex)
    raise ex from orig_exception


def epi_transliterate_word_cached(word: str, logger: Logger) -> str:
  # I am assuming there is no IPA difference in EPITRAN.
  word = word.lower()

  if word in EPITRAN_EN_WORD_CACHE:
    return EPITRAN_EN_WORD_CACHE[word]

  res = epi_transliterate_word_verbose(word, logger)

  EPITRAN_EN_WORD_CACHE[word] = res

  return res


def epi_transliterate_word_verbose(word: str, logger: Logger) -> str:
  global EPITRAN_CACHE
  assert Language.ENG in EPITRAN_CACHE

  res = epi_transliterate_without_logging(EPITRAN_CACHE[Language.ENG], word)
  # res = EPITRAN_CACHE[Language.ENG].transliterate(word)

  logger.info(f"used Epitran for: {word} => {res}")
  return res


def epi_transliterate_without_logging(epi_instance: Epitran, word: str) -> str:
  main_logger = getLogger()
  old_level = main_logger.level
  main_logger.setLevel(WARNING)

  result = epi_instance.transliterate(word)

  main_logger.setLevel(old_level)

  return result


def en_to_ipa_cmu(text: str, replace_unknown_with: str, logger: Logger) -> str:
  assert replace_unknown_with is not None
  global CMU_CACHE

  ensure_cmudict_is_loaded(logger)

  try:
    result = CMU_CACHE.sentence_to_ipa(
      sentence=text,
      replace_unknown_with=replace_unknown_with
    )
    return result
  except Exception as orig_exception:
    ex = ValueError(f"Conversion of '{text}' was not successfull!")
    logger.error("", exc_info=ex)
    raise ex from orig_exception


def ger_to_ipa(text: str, logger: Logger) -> str:
  if is_phonetic_transcription_in_text(text):
    words = text.split(" ")
    ipa_list = [ipa_of_phonetic_transcription(word)
                if is_phonetic_transcription(word)
                else ger_ipa_of_text_not_containing_phonetic_transcription(text=word, logger=logger)
                for word in words]
    res = " ".join(ipa_list)
    return res
  return ger_ipa_of_text_not_containing_phonetic_transcription(text, logger)


def ger_ipa_of_text_not_containing_phonetic_transcription(text: str, logger: Logger) -> str:
  global EPITRAN_CACHE
  ensure_ger_epitran_is_loaded(logger)
  result = epi_transliterate_without_logging(EPITRAN_CACHE[Language.GER], text)
  # result = EPITRAN_CACHE[Language.GER].transliterate(text)
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


def text_normalize(text: str, lang: Language, logger: Logger) -> str:
  if lang == Language.ENG:
    return normalize_en(text)

  if lang == Language.GER:
    return normalize_ger(text)

  if lang == Language.CHN:
    return normalize_chn(text)

  if lang == Language.IPA:
    return normalize_ipa(text)

  assert False


def clear_en_word_cache() -> None:
  EPITRAN_EN_WORD_CACHE.clear()


def text_to_ipa(text: str, lang: Language, mode: Optional[EngToIpaMode], replace_unknown_with: Optional[str], logger: Logger, use_cache: bool = True) -> str:
  if lang == Language.ENG:
    if mode is None:
      ex = ValueError(f"Parameter mode is required for {lang!r}!")
      logger.error("", exc_info=ex)
      raise ex

    return en_to_ipa(
      text=text,
      mode=mode,
      replace_unknown_with=replace_unknown_with,
      use_cache=use_cache,
      logger=logger,
    )

  if lang == Language.GER:
    return ger_to_ipa(text, logger)

  if lang == Language.CHN:
    return chn_to_ipa(text)

  if lang == Language.IPA:
    return text

  assert False


def text_to_sentences(text: str, lang: Language, logger: Logger) -> List[str]:
  if lang == Language.CHN:
    return split_chn_text(text)

  if lang == Language.IPA:
    return split_ipa_text(text)

  if lang == Language.ENG:
    return split_en_text(text)

  if lang == Language.GER:
    return split_ger_text(text)

  assert False


def text_to_symbols(text: str, lang: Language, ipa_settings: Optional[IPAExtractionSettings], logger: Logger) -> List[str]:
  if lang in (Language.ENG, Language.GER, Language.CHN):
    return list(text)
  if lang == Language.IPA:
    if ipa_settings is None:
      ex = ValueError(f"You have to pass ipa_settings for {lang!r}!")
      logger.error("", exc_info=ex)
      raise ex

    return extract_from_sentence(
      text,
      ipa_settings,
      logger,
    )

  assert False


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


def chn_to_ipa(chn: str) -> str:
  res_str = chn_sentence_to_ipa(chn)
  for regex, replacement in CHN_SUBS:
    res_str = re.sub(regex, replacement, res_str)

  return res_str


def chn_word_to_ipa(word: str) -> str:
  if is_phonetic_transcription(word):
    return ipa_of_phonetic_transcription(word)
  return chn_ipa_of_word_not_containing_phonetic_transcription(word)


def chn_sentence_to_ipa(sentence: str) -> str:
  chn_words = split_chn_sentence(sentence)
  res = [chn_word_to_ipa(word) for word in chn_words]
  res_str = ' '.join(res)
  return res_str


def chn_ipa_of_word_not_containing_phonetic_transcription(word: str) -> str:
  assert not is_phonetic_transcription(word)
  chn_ipa = hanzi.to_ipa(word)
  chn_ipa = chn_ipa.replace(' ', '')
  return chn_ipa
