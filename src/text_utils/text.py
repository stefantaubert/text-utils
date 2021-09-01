from enum import IntEnum
from logging import Logger
from typing import List, Optional, Tuple

from nltk import download
from nltk.tokenize import sent_tokenize
from unidecode import unidecode as convert_to_ascii

from text_utils.adjustments import (collapse_whitespace, expand_abbreviations,
                                    expand_units_of_measure, normalize_numbers,
                                    replace_at_symbols,
                                    replace_big_letter_abbreviations,
                                    replace_mail_addresses)
from text_utils.chinese_wrapper import chn_to_ipa, split_chn_text
from text_utils.cmudict_wrapper import en_to_ipa_cmu, en_to_ipa_cmu_epitran
from text_utils.epitran_wrapper import en_to_ipa_epitran, ger_to_ipa
from text_utils.ipa2symb import (IPAExtractionSettings, extract_from_sentence,
                                 ipa_of_phonetic_transcription,
                                 is_phonetic_transcription,
                                 is_phonetic_transcription_in_text)
from text_utils.language import Language
from text_utils.utils import split_text

IPA_SENTENCE_SEPARATORS = [r"\?", r"\!", r"\."]


class EngToIpaMode(IntEnum):
  EPITRAN = 0
  CMUDICT = 1
  BOTH = 2


def get_ngrams(sentence_symbols: List[str], n: int) -> List[Tuple[str]]:
  if n < 1:
    raise Exception()

  res: List[Tuple[str]] = []
  for i in range(len(sentence_symbols) - n + 1):
    tmp = tuple(sentence_symbols[i:i + n])
    res.append(tmp)
  return res


def en_to_ipa(text: str, mode: EngToIpaMode, replace_unknown_with: Optional[str], use_cache: bool, consider_ipa_annotations: bool, logger: Logger) -> str:
  assert mode is not None
  if consider_ipa_annotations and is_phonetic_transcription_in_text(text):
    words = text.split(" ")
    ipa_list = [
      ipa_of_phonetic_transcription(word, logger)
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


def text_to_ipa(text: str, lang: Language, mode: Optional[EngToIpaMode], replace_unknown_with: Optional[str], logger: Logger, consider_ipa_annotations: bool = False, use_cache: bool = True) -> str:
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
      consider_ipa_annotations=consider_ipa_annotations,
      logger=logger,
    )

  if lang == Language.GER:
    return ger_to_ipa(text, consider_ipa_annotations, logger)

  if lang == Language.CHN:
    return chn_to_ipa(text, logger)

  if lang == Language.IPA:
    # maybe check is valid IPA
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


def sentence_to_words(sentence_symbols: List[str]) -> List[List[str]]:
  if len(sentence_symbols) == 0:
    return []
  res = []
  current_word = []
  for symbol in sentence_symbols:
    if symbol == " ":
      res.append(current_word)
      current_word = []
    else:
      current_word.append(symbol)
  res.append(current_word)
  return res


def words_to_sentence(words: List[List[str]]) -> List[str]:
  res = []
  for i, word in enumerate(words):
    res.extend(word)
    is_last_word = i == len(words) - 1
    if not is_last_word:
      res.append(" ")
  return res


def strip_word(word: List[str], symbols: List[str]) -> List[str]:
  res = []
  for i, char in enumerate(word):
    if char in symbols:
      continue
    res = word[i:]
    break

  for i in range(len(res)):
    char = res[-1 - i]
    if char in symbols:
      continue
    res = res[:len(res) - i]
    break
  return res


def symbols_to_lower(symbols: List[str]) -> List[str]:
  res = []
  for symbol in symbols:
    res.append(symbol.lower())
  return res


def symbols_replace(symbols: List[str], search_for: List[str], replace_with: List[str], ignore_case: bool) -> List[str]:
  new_symbols = symbols.copy()
  start_index = is_sublist(
      search_in=new_symbols,
      search_for=search_for,
      ignore_case=ignore_case
  )
  if start_index == -1:
    return new_symbols

  delete_and_insert_in_list(
    main_list=new_symbols,
    list_to_delete=search_for,
    list_to_insert=replace_with,
    start_index=start_index
  )
  if is_sublist(
    search_in=new_symbols,
    search_for=search_for,
    ignore_case=ignore_case
  ) != -1:
    new_symbols = symbols_replace(new_symbols, search_for, replace_with, ignore_case)
  return new_symbols


def delete_and_insert_in_list(main_list: List[str], list_to_delete: List[str], list_to_insert: List[str], start_index: int) -> None:
  del main_list[start_index:start_index + len(list_to_delete)]
  end_slice = main_list[start_index:]
  del main_list[start_index:]
  main_list.extend(list_to_insert)
  main_list.extend(end_slice)


def is_sublist(search_in: List[str], search_for: List[str], ignore_case: bool) -> int:
  len_search_in, len_search_for = len(search_in), len(search_for)
  aux_search_in = upper_list_if_true(search_in, ignore_case)
  aux_search_for = upper_list_if_true(search_for, ignore_case)
  for i in range(len_search_in):
    if aux_search_in[i:i + len_search_for] == aux_search_for:
      return i
  return -1


def upper_list_if_true(l: List[str], upper: bool) -> List[str]:
  if upper:
    upper_l = [element.upper() for element in l]
    return upper_l
  return l


def text_to_symbols(text: str, lang: Language, ipa_settings: Optional[IPAExtractionSettings], logger: Logger, merge_stress: Optional[bool] = True) -> List[str]:
  if lang in (Language.ENG, Language.GER, Language.CHN):
    return list(text)
  if lang == Language.IPA:
    if ipa_settings is None:
      ex = ValueError(f"You have to pass ipa_settings for {lang!r}!")
      logger.error("", exc_info=ex)
      raise ex

    return extract_from_sentence(
      ipa_sentence=text,
      settings=ipa_settings,
      merge_stress=merge_stress,
    )

  assert False


def split_en_text(text: str) -> List[str]:
  download('punkt', quiet=True)
  res = sent_tokenize(text, language="english")
  return res


def split_ger_text(text: str) -> List[str]:
  download('punkt', quiet=True)
  res = sent_tokenize(text, language="german")
  return res


def split_ipa_text(text: str) -> List[str]:
  return split_text(text, IPA_SENTENCE_SEPARATORS)
