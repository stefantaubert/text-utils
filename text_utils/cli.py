


from text_utils.symbols_map import SymbolsMap


def print_map(path: str):
  symbols_map = SymbolsMap.load(path)
  for map_output, map_input in symbols_map.items():
    print(f"{map_input} -> {map_output}")


print_map("text_utils/examplemap.json")


def print_symbols(path: str):
  with open(path) as f:
    liste = f.readlines()
    printlist = []
    for l in liste:
      l = l.strip()
      if len(l) > 0:
        l = l[1:-1]
        printlist.append(l)
  print(", ".join(printlist))


print_symbols("text_utils/examplesymbols.symb")
