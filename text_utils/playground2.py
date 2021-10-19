# dic = {"a": "b", "c": "d"}

# for pos, (value, key) in enumerate(dic.items()):
#   print(pos, key)

# for pos, x in enumerate(dic):
#   value, key = x
#   print(pos, key)

# from text_utils.print_or_change_map_and_symbols import print_map

# print('\033[1m' + "expample" + '\033[0m')
# print("example")
# #print('\033[1m' + f"{map_input} \u2192 {map_output}" + '\033[0m')

# print_map("text_utils/examplemap.json")

def open_file_and_print_symbols(lines) -> int:
  number_of_lines = 0
  contains_nothing = False
  for pos, line in enumerate(lines):
    line = line.strip()
    if len(line) > 0:
      line = line[1:-1]
      if line == "":
        contains_nothing = True
      print(f"{pos+1}: {line}")
      number_of_lines = pos + 1
  if not contains_nothing:
    number_of_lines += 1
    print(f"{number_of_lines}: NOTHING")
  return number_of_lines


symbol_path = "text_utils/examplesymbols.symb"

with open(symbol_path) as symbol_file:
  lines = symbol_file.readlines()
number_of_lines = open_file_and_print_symbols(lines)
