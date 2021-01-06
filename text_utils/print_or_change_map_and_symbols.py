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
  parser.add_argument("-a", "--arrow_type", type=str, required=False,
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
