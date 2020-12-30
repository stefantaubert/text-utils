from argparse import ArgumentParser
from typing import Mapping, Tuple

from text_utils.symbols_map import SymbolsMap


def init_map_parser(parser: ArgumentParser):
  parser.add_argument("-p", "--path", type=str, required=True,
                      help="Path to .json-file containing the map")
  return print_map


def print_map(path: str):
  symbols_map = SymbolsMap.load(path)
  for map_output, map_input in symbols_map.items():
    print(f"{map_input} \u2192 {map_output}")


def init_symbol_parser(parser: ArgumentParser):
  parser.add_argument("-p", "--path", type=str, required=True,
                      help="Path to file containing the symbols")
  return print_symbols


def print_symbols(path: str):
  with open(path) as symbol_file:
    lines = symbol_file.readlines()
    print_list = []
    for line in lines:
      line = line.strip()
      if len(line) > 0:
        line = line[1:-1]
        print_list.append(line)
  print(", ".join(print_list))


def init_change_parser(parser: ArgumentParser):
  parser.add_argument("-p", "--map_path", type=str, required=True,
                      help="Path to .json-file containing the map")
  parser.add_argument("-s", "--symbol_path", type=str, required=True,
                      help="Path to file containing the allowed symbols")
  return change_symbols_in_map


def change_symbols_in_map(map_path: str, symbol_path: str):
  update = True
  input_map = SymbolsMap.load(map_path)
  while update:
    change_one_symbol_in_map(input_map, map_path, symbol_path)
    continue_updating = input("Do you want to adjust another symbol? [y]/n: ")
    update = continue_updating in ["y", ""]


def change_one_symbol_in_map(input_map: SymbolsMap, map_path: str, symbol_path: str):
  chosen_key = choose_key(input_map)
  chosen_symbol = choose_symbol(symbol_path)
  input_map[chosen_key] = chosen_symbol
  input_map.save(map_path)
  print("Updated Map:")
  print_map(map_path)


def choose_key(input_map: SymbolsMap) -> str:
  print("The symbol corresponding to which key should be adjusted? Please input the corresponding number.")
  chosen_key = ""
  for pos, (key, _) in enumerate(input_map.items()):
    print(f"{pos+1}: {key}")
  chosen_key_pos = get_correct_input(len(input_map))
  for pos, (key, _) in enumerate(input_map.items()):
    if pos == chosen_key_pos:
      chosen_key = key
  return chosen_key


def choose_symbol(symbol_path) -> str:
  print("Which symbol shoud be assigned to the chosen key? Please input the corresponding number.")
  with open(symbol_path) as symbol_file:
    lines = symbol_file.readlines()
  number_of_lines = open_file_and_print_symbols(lines)
  chosen_symbol_pos = get_correct_input(number_of_lines)
  chosen_symbol = lines[chosen_symbol_pos].strip()[1:-1]
  return chosen_symbol


def open_file_and_print_symbols(lines) -> int:
  number_of_lines = 0
  for pos, line in enumerate(lines):
    line = line.strip()
    if len(line) > 0:
      line = line[1:-1]
      print(f"{pos+1}: {line}")
      number_of_lines = pos + 1
  return number_of_lines


def get_correct_input(upper_bound: int) -> int:
  pos = int(input("Your input: ")) - 1
  while pos < 0 or pos >= upper_bound:
    pos = int(input(f"Please input a number between 1 and {upper_bound}: ")) - 1
  return pos
