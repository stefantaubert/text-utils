from logging import getLogger
from pathlib import Path
from typing import List, Optional

from text_utils.symbols_map import SymbolsMap
from text_utils.types import Symbol

NOTHING = "NOTHING"
SPACE = "SPACE"
WEIGHTS_ARROW_TYPE = "weights"
INFERENCE_ARROW_TYPE = "inference"
LEFT_ARROW = "\u2190"
RIGHT_ARROW = "\u2192"


def print_map(path: Path, arrow_type: str) -> None:
  print_headline(arrow_type)
  symbols_map = SymbolsMap.load(path)
  for map_input, map_output in symbols_map.items():
    if arrow_type == WEIGHTS_ARROW_TYPE:
      string_to_print = f"{get_symbol_representation(map_output)} {arrow(arrow_type)} {get_symbol_representation(map_input)}"
    else:
      string_to_print = f"{get_symbol_representation(map_input)} {arrow(arrow_type)} {get_symbol_representation(map_output)}"

    print_bold_or_normal(string_to_print, map_input != map_output)


def print_headline(arrow_type: str) -> None:
  if arrow_type == "weights":
    headline = f"Trained symbol {RIGHT_ARROW} symbol to be trained"
  else:
    headline = f"Occurring symbol in input {LEFT_ARROW} synthesizable symbol"
  print('\033[1m' + '\033[4m' + headline + '\033[0m')


def arrow(arrow_type: str) -> str:
  return RIGHT_ARROW if arrow_type == WEIGHTS_ARROW_TYPE else LEFT_ARROW


def print_bold_or_normal(string_to_print: str, bold: bool) -> None:
  if bold:
    print_bold(string_to_print)
  else:
    print(string_to_print)


def print_bold(string_to_print: str) -> None:
  print('\033[1m' + string_to_print + '\033[0m')


def get_symbol_representation(symbol: str) -> str:
  if symbol == "":
    return NOTHING
  if symbol == " ":
    return SPACE
  return symbol


def print_symbols(path: Path) -> None:
  with open(path, mode="r") as symbol_file:
    lines = symbol_file.readlines()
    print_list = []
    for line in lines:
      line = line.strip()
      if len(line) > 0:
        line = line[1:-1]
        print_list.append(get_symbol_representation(line))
  print(", ".join(print_list))


def change_symbols_in_map(map_path: Path, symbol_path: Path, arrow_type: Optional[str] = None, to_key: Optional[Symbol] = None, map_symbol: Optional[Symbol] = None) -> None:
  input_map = SymbolsMap.load(map_path)
  if to_key is None and map_symbol is None:
    if arrow_type is None:
      print("You have to specify the arrow type.")
      return
    update = True
    while update:
      change_one_symbol_in_map(input_map, map_path, symbol_path, arrow_type)
      continue_updating = input("Do you want to adjust another symbol? [y]/n: ")
      update = continue_updating in ["y", ""]
  elif (to_key is None and map_symbol is not None) or (to_key is not None and map_symbol is None):
    print("You have to either specify both the key and the symbol or none of them.")
  elif not (is_given_symbol_in_symbolfile(map_symbol, symbol_path) or map_symbol == ""):
    print("The symbol you've chosen is not one of the allowed symbols.")
  elif to_key not in input_map.keys():
    print("The key you've specified is not in the map.")
  else:
    input_map[to_key] = map_symbol
    input_map.save(map_path)


def is_given_symbol_in_symbolfile(symbol: Symbol, symbol_path: Path) -> bool:
  logger = getLogger(__name__)
  with open(symbol_path) as symbol_file:
    lines = symbol_file.readlines()
    for line in lines:
      line = line.strip()
      if len(line) > 0:
        line = line[1:-1]
        #logger.info(f"{symbol} - {line}, {symbol == line}")
        if symbol == line:
          return True
  return False


def change_one_symbol_in_map(input_map: SymbolsMap, map_path: Path, symbol_path: Path, arrow_type: str) -> None:
  chosen_key = choose_key(input_map, arrow_type)
  old_symbol = input_map[chosen_key]
  chosen_symbol = choose_symbol(symbol_path, old_symbol, chosen_key)
  input_map[chosen_key] = chosen_symbol
  input_map.save(map_path)
  print("Updated Map:")
  print_map(map_path, arrow_type)


def choose_key(input_map: SymbolsMap, arrow_type: str) -> str:
  print("The symbol corresponding to which key should be adjusted? Please input the corresponding number.")
  chosen_key = ""
  for pos, (key, value) in enumerate(input_map.items()):
    string_to_print = f"{pos+1}: {get_symbol_representation(key)} ({arrow(arrow_type)} {get_symbol_representation(value)})"
    print_bold_or_normal(string_to_print, key != value)
  chosen_key_pos = get_correct_input(len(input_map))
  for pos, (key, _) in enumerate(input_map.items()):
    if pos == chosen_key_pos:
      chosen_key = key
  return chosen_key


def choose_symbol(symbol_path: Path, old_symbol: Symbol, chosen_key: Symbol) -> str:
  print(
    f"Which new symbol instead of {get_symbol_representation(old_symbol)} should be assigned to {get_symbol_representation(chosen_key)}? Please input the corresponding number.")
  with open(symbol_path) as symbol_file:
    lines = symbol_file.readlines()
  number_of_lines = open_file_and_print_symbols(lines)
  chosen_symbol_pos = get_correct_input(number_of_lines)
  if chosen_symbol_pos < number_of_lines - 1:
    chosen_symbol = lines[chosen_symbol_pos].strip()[1:-1]
  else:
    chosen_symbol = ""
  return chosen_symbol


def open_file_and_print_symbols(file_lines: List[str]) -> int:
  number_of_lines = 0
  contains_nothing = False
  for pos, line in enumerate(file_lines):
    line = line.strip()
    if len(line) > 0:
      line = line[1:-1]
      if line == "":
        contains_nothing = True
      print(f"{pos+1}: {get_symbol_representation(line)}")
      number_of_lines = pos + 1
  if not contains_nothing:
    number_of_lines += 1
    print(f"{number_of_lines}: {NOTHING}")
  return number_of_lines


def get_correct_input(upper_bound: int) -> int:
  user_input = input("Your input: ")
  while (not user_input.isnumeric()) or (int(user_input) < 1 or int(user_input) > upper_bound):
    user_input = input(f"Please input a number between 1 and {upper_bound}: ")
  pos = int(user_input) - 1
  return pos
