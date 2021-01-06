from argparse import ArgumentParser

from text_utils.symbols_map import SymbolsMap


def init_map_parser(parser: ArgumentParser):
  parser.add_argument("-p", "--path", type=str, required=True,
                      help="Path to .json-file containing the map")
  parser.add_argument("-a", "--arrow_type", type=str, required=False,
                      help="Sets the direction of the arrow")
  return print_map


def print_map(path: str, arrow_type: str):
  symbols_map = SymbolsMap.load(path)
  arrow = get_correct_type_input(arrow_type)
  for map_output, map_input in symbols_map.items():
    string_to_print = f"{space_or_nothing_as_word(map_input)} {arrow} {space_or_nothing_as_word(map_output)}"
    if map_input == map_output:
      print(string_to_print)
    else:
      print('\033[1m' + string_to_print + '\033[0m')


def space_or_nothing_as_word(symbol: str) -> str:
  if symbol == "":
    return "NOTHING"
  if symbol == " ":
    return "SPACE"
  return symbol


def get_correct_type_input(arrow_type: str) -> str:
  while arrow_type not in ["weights", "interference"]:
    arrow_type = input(
      "Type must be either \"weights\" or \"interference\". Please define the type again: ")
  arrow = "\u2190" if arrow_type == "interference" else "\u2192"
  return arrow


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
        print_list.append(space_or_nothing_as_word(line))
  print(", ".join(print_list))
