from argparse import ArgumentParser
from typing import Callable

from text_utils.symbols_map import SymbolsMap

NOTHING = "NOTHING"
SPACE = "SPACE"
WEIGHTS = "weights"
INFERENCE = "inference"
ARROW_TYPES = [WEIGHTS, INFERENCE]
LEFT_ARROW = "\u2190"
RIGHT_ARROW = "\u2192"


def init_map_parser(parser: ArgumentParser) -> Callable[[str, str], None]:
  parser.add_argument("-p", "--path", type=str, required=True,
                      help="Path to .json-file containing the map")
  parser.add_argument("-a", "--arrow_type", type=str, required=True,
                      help="Sets the direction of the arrow", choices=ARROW_TYPES)
  return print_map


def print_map(path: str, arrow_type: str) -> None:
  symbols_map = SymbolsMap.load(path)
  arrow = LEFT_ARROW if arrow_type == INFERENCE else RIGHT_ARROW
  for map_output, map_input in symbols_map.items():
    string_to_print = f"{get_symbol_representation(map_input)} {arrow} {get_symbol_representation(map_output)}"
    print_bold_or_normal(string_to_print, map_input != map_output)


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


def init_symbol_parser(parser: ArgumentParser) -> Callable[[str], None]:
  parser.add_argument("-p", "--path", type=str, required=True,
                      help="Path to file containing the symbols")
  return print_symbols


def print_symbols(path: str) -> None:
  with open(path) as symbol_file:
    lines = symbol_file.readlines()
    print_list = []
    for line in lines:
      line = line.strip()
      if len(line) > 0:
        line = line[1:-1]
        print_list.append(get_symbol_representation(line))
  print(", ".join(print_list))


def init_change_parser(parser: ArgumentParser):
  parser.add_argument("-p", "--map_path", type=str, required=True,
                      help="Path to .json-file containing the map")
  parser.add_argument("-s", "--symbol_path", type=str, required=True,
                      help="Path to file containing the allowed symbols")
  parser.add_argument("-a", "--arrow_type", type=str, required=True,
                      help="Sets the direction of the arrow", choices=["weights", "inference"])
  parser.add_argument("--map", type=str, required=False,
                      help="Key to which new symbol should be assigned")
  parser.add_argument("--to", type=str, required=False,
                      help="Symbol that should be assigned to chosen key")
  return change_symbols_in_map


def change_symbols_in_map(map_path: str, symbol_path: str, arrow_type: str, map: str = None, to: str = None):
  input_map = SymbolsMap.load(map_path)
  if map is None and to is None:
    update = True
    while update:
      change_one_symbol_in_map(input_map, map_path, symbol_path, arrow_type)
      continue_updating = input("Do you want to adjust another symbol? [y]/n: ")
      update = continue_updating in ["y", ""]
  elif map is None and to is not None or map is not None and to is None:
    print("You have to either specify both the key and the symbol or none of them.")
  elif not is_given_symbol_in_symbolfile(map, symbol_path):
    print("The symbol you've chosen is not one of the allowed symbols.")
  elif to not in input_map.values():
    print("The key you've specified is not in the map.")
  else:
    input_map[to] = map
    input_map.save(map_path)


def is_given_symbol_in_symbolfile(symbol: str, symbol_path: str) -> bool:
  with open(symbol_path) as symbol_file:
    lines = symbol_file.readlines()
    for line in lines:
      line = line.strip()
      if len(line) > 0:
        line = line[1:-1]
        if symbol == line:
          return True
  return False


def change_one_symbol_in_map(input_map: SymbolsMap, map_path: str, symbol_path: str, arrow_type: str):
  chosen_key = choose_key(input_map, arrow_type)
  chosen_symbol = choose_symbol(symbol_path)
  input_map[chosen_key] = chosen_symbol
  input_map.save(map_path)
  print("Updated Map:")
  print_map(map_path, arrow_type)


def choose_key(input_map: SymbolsMap, arrow_type: str) -> str:
  print("The symbol corresponding to which key should be adjusted? Please input the corresponding number.")
  chosen_key = ""
  for pos, (key, value) in enumerate(input_map.items()):
    string_to_print = f"{pos+1}: {key} ({reverse_arrow(arrow_type)} {get_symbol_representation(value)})"
    print_bold_or_normal(string_to_print, key != value)
  chosen_key_pos = get_correct_input(len(input_map))
  for pos, (key, _) in enumerate(input_map.items()):
    if pos == chosen_key_pos:
      chosen_key = key
  return chosen_key


def reverse_arrow(arrow_type: str) -> str:
  return "\u2190" if arrow_type == "weights" else "\u2192"


def choose_symbol(symbol_path) -> str:
  print("Which symbol shoud be assigned to the chosen key? Please input the corresponding number.")
  with open(symbol_path) as symbol_file:
    lines = symbol_file.readlines()
  number_of_lines = open_file_and_print_symbols(lines)
  chosen_symbol_pos = get_correct_input(number_of_lines)
  if chosen_symbol_pos < number_of_lines - 1:
    chosen_symbol = lines[chosen_symbol_pos].strip()[1:-1]
  else:
    chosen_symbol = "NOTHING"
  return chosen_symbol


def open_file_and_print_symbols(lines) -> int:
  number_of_lines = 0
  contains_nothing = False
  for pos, line in enumerate(lines):
    line = line.strip()
    if len(line) > 0:
      line = line[1:-1]
      if line == "":
        contains_nothing = True
      print(f"{pos+1}: {get_symbol_representation(line)}")
      number_of_lines = pos + 1
  if not contains_nothing:
    number_of_lines += 1
    print(f"{number_of_lines}: NOTHING")
  return number_of_lines


def get_correct_input(upper_bound: int) -> int:
  user_input = input("Your input: ")
  while (not user_input.isnumeric()) or (int(user_input) < 1 or int(user_input) > upper_bound):
    user_input = input(f"Please input a number between 1 and {upper_bound}: ")
  pos = int(user_input) - 1
  return pos
