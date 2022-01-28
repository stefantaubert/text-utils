from typing import Generator

from text_utils.types import Symbol


def can_serialize(text: str, split_symbol: Symbol) -> bool:
  if split_symbol * 2 in text:
    if not split_symbol * 3 in text:
      pass


def str_deserialization(text: str, split_symbol: Symbol) -> Generator[Symbol, None, None]:
  #assert can_serialize(text, split_symbol)
  symbol = ""
  split_symbol_before = False
  for char in text:
    if char != split_symbol:
      symbol += char
    elif symbol != "":
      yield symbol
      symbol = ""
      split_symbol_before = True
    elif split_symbol_before:
      yield split_symbol
      split_symbol_before = False
    else:
      split_symbol_before = True
  yield symbol
  # elif symbol == "" and not split_symbol_before:
  #   split_symbol_before = True
  # else:
  #   yield symbol
  #   yield split_symbol
  #   symbol = ""


# def str_deserialization4(text: str, split_symbol: Symbol) -> Generator[Symbol, None, None]:
#   #assert can_serialize(text, split_symbol)
#   symbol = ""
#   for index, char in enumerate(text):
#     if char != split_symbol:
#       symbol += char
#     elif symbol == "":
#       if symbol[index + 1] != split_symbol:
#         continue
#       if symbol[index + 3] ==
#     else:
#       yield symbol
#       symbol = ""


def str_deserialization3(text: str, split_symbol: Symbol) -> Generator[Symbol, None, None]:
  #assert can_serialize(text, split_symbol)
  symbol = ""
  for char in text:
    if char != split_symbol:
      symbol += char
    # elif symbol == "":
    #   if symbol[1] == split_symbol:
    #     yield split_symbol

    else:
      yield symbol
      #text = text[len(symbol):]
      symbol = ""


def str_serialization2(text: str, split_symbol: Symbol) -> Generator[Symbol, None, None]:
  #assert can_serialize(text, split_symbol)
  all_words = []
  word = []
  for char in text:
    if char != split_symbol:
      word.append(char)
    elif word == []:
      if word[1] == split_symbol:
        yield split_symbol

      # len_split_symbol_sequence = 1
      # for following_char in word[1:]:
      #   if following_char == split_symbol:
      #     len_split_symbol_sequence += 1
      #   else:
      #     yield

    else:
      word = "".join(word)
      yield(word)
      word = []
      text = text[len(word):]
