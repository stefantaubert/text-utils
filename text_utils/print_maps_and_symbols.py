from argparse import ArgumentParser

from text_utils.symbols_map import SymbolsMap


def init_map_parser(parser: ArgumentParser):
  parser.add_argument("-p", "--path", type=str, required=True,
                      help="Path to .json-file containing the map")
  return print_map


def print_map(path: str):
  symbols_map = SymbolsMap.load(path)
  for map_output, map_input in symbols_map.items():
    print(f"{map_input} \u2192 {map_output}")


# print_map("text_utils/examplemap.json")

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


# print_symbols("text_utils/examplesymbols.symb")
