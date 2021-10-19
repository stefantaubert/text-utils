import re
import string

from text_utils.pronunciation.ipa2symb import (merge_left, merge_right,
                                               merge_together)

# symbols = ("abc", "&", "d")
# res = merge_together(symbols, {"&"}, {})
# print(res)
# res = merge_left(symbols, {"&"}, {})
# print(res)
# res = merge_right(symbols, {"&"}, {})
# print(res)

res = merge_right(("de", "&", "bc"), merge_symbols={"&"}, ignore_merge_symbols={"a"})
print(res)

"""
def merge_together(symbols: Symbols, merge_symbols: Set[Symbol], ignore_merge_symbols: Set[Symbol]) -> Symbols:
  merged_left = merge_left(symbols, merge_symbols, ignore_merge_symbols)
  merged_final = merge_right(merged_left, merge_symbols, ignore_merge_symbols)
  return merged_final
falsch, produziert aus
symbols = ("abc", "&", "d")
res = merge_together(symbols, {"&"}, {})
den Output
('abc', '&d')
weil "&d" kein merge symbol ist
"""
# def merge_together(symbols: Symbols, merge_symbols: Set[Symbol], ignore_merge_symbols: Set[Symbol]) -> Symbols:
#   merge_or_ignore_merge_symbols = merge_symbols.union(ignore_merge_symbols)
#   j = 0
#   merged_symbols = []
#   while j < len(symbols):
#     new_symbol = symbols[j]
#     store_j = j
#     j += 1
#     if new_symbol not in merge_or_ignore_merge_symbols:
#       merge_symbol_concat, index = get_all_next_merge_symbols(symbols[j:], merge_symbols)
#       while j+1 < len(symbols) and symbols[j] in merge_symbols and symbols[j+1] not in merge_or_ignore_merge_symbols:
#         new_symbol = new_symbol + symbols[j] + symbols[j+1]
#         j += 2
#     merged_symbols.append(new_symbol)
#   return tuple(merged_symbols)
