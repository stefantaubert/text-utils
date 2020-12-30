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


# def change_symbols_in_map(map_path: str, symbol_path: str):
#   input_map = SymbolsMap.load(map_path)
#   print("The symbol corresponding to which key should be adjusted? Please input the corresponding number.")
#   for pos, (key, _) in enumerate(input_map.items()):
#     print(f"{pos+1}: {key}")
#   chosen_key_pos = int(input("Your input: ")) - 1
#   for pos, (key, _) in enumerate(input_map.items()):
#     if pos == chosen_key_pos:
#       chosen_key = key
#   assert chosen_key
#   print("Which symbol shoud be assigned to the chosen key? Please input the corresponding number.")
#   with open(symbol_path) as symbol_file:
#     lines = symbol_file.readlines()
#     for pos, line in enumerate(lines):
#       line = line.strip()
#       if len(line) > 0:
#         line = line[1:-1]
#         print(f"{pos+1}: {line}")
#   chosen_symbol_pos = int(input("Your input: ")) - 1
#   with open(symbol_path) as symbol_file:
#     lines = symbol_file.readlines()
#     for pos, line in enumerate(lines):
#       if pos == chosen_symbol_pos:
#         chosen_symbol = line.strip()[1:-1]
#   input_map[chosen_key] = chosen_symbol
#   input_map.save(map_path)
#   print("Updated Map:")
#   print_map(map_path)

def change_symbols_in_map(map_path: str, symbol_path: str):
  input_map = SymbolsMap.load(map_path)
  update = True
  while update:
    print("The symbol corresponding to which key should be adjusted? Please input the corresponding number.")
    for pos, (key, _) in enumerate(input_map.items()):
      print(f"{pos+1}: {key}")
    chosen_key_pos = int(input("Your input: ")) - 1
    while chosen_key_pos < 0 or chosen_key_pos >= len(input_map):
      chosen_key_pos = int(input(f"Please input a number between 1 and {len(input_map)}: ")) - 1
      #raise ValueError(f"Please input a number between 1 and {len(input_map)}.")
    for pos, (key, _) in enumerate(input_map.items()):
      if pos == chosen_key_pos:
        chosen_key = key
    assert chosen_key
    print("Which symbol shoud be assigned to the chosen key? Please input the corresponding number.")
    with open(symbol_path) as symbol_file:
      lines = symbol_file.readlines()
      for pos, line in enumerate(lines):
        line = line.strip()
        if len(line) > 0:
          line = line[1:-1]
          print(f"{pos+1}: {line}")
        number_of_lines = pos - 1
    chosen_symbol_pos = int(input("Your input: ")) - 1
    while chosen_symbol_pos < 0 or chosen_symbol_pos >= number_of_lines:
      chosen_symbol_pos = int(input(f"Please input a number between 1 and {number_of_lines}: ")) - 1
    with open(symbol_path) as symbol_file:
      lines = symbol_file.readlines()
      for pos, line in enumerate(lines):
        if pos == chosen_symbol_pos:
          chosen_symbol = line.strip()[1:-1]
    input_map[chosen_key] = chosen_symbol
    input_map.save(map_path)
    print("Updated Map:")
    print_map(map_path)
    continue_updating = input("Do you want to adjust another symbol? y/n: ")
    update = continue_updating == "y"
