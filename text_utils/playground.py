from collections import OrderedDict
from typing import Dict, List
from typing import OrderedDict as OrderedDictType
from typing import Set, TypeVar

import numpy as np

T = TypeVar('T')

liste = [1, 2, 34, 5, 6]
print(3 * liste)
print(type(liste))

# def from_intersection(map_from: set, map_to: set):
#   #only_a = list(sorted(list(symbolsA)))
#   in_both = list(sorted(list(map_from.intersection(map_to))))
#   sym_mapping = ([(symb, symb) for symb in in_both])

#   symbs_in_map_to_without_mapping = map_to.difference(map_from)
#   for symb in get_sorted_list_from_set(symbs_in_map_to_without_mapping):
#     sym_mapping[symb] = ""

#   return sym_mapping


# def get_sorted_list_from_set(unsorted_set: Set[T]) -> List[T]:
#   res: List[T] = list(sorted(list(unsorted_set)))
#   return res


# a = {3, 1, 5, 7}
# b = {1, 2, 3}

# print(from_intersection(a, b))

# # def print_symbols(path: str):
# #   symbol_file = open(path, "r")
# #   symbols = symbol_file.read()
# #   symbols.replace("\n", "")
# #   print(symbols)
# #   symbol_list = [symbol[1:-1]
# #                  if symbol[0] == "\"" and symbol[-1] == "\""
# #                  else symbol for symbol in symbols]
# #   for symbol in symbol_list:
# #     print("3")


# LINE = re.compile(r"\s*\"(.+)\"\s*")
# def print_symbols(path: str):
#   symbol_file = open(path, "r")
#   for line in symbol_file:
#     line = line.strip().strip("\"")
#     #line_without_linebreak_and_quotation_marks = LINE.match(line)
#     #assert line_without_linebreak_and_quotation_marks
#     #print(line_without_linebreak_and_quotation_marks.group(1))
#     print(line)
