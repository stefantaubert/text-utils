def test_get_next_merged_symbol_and_index__from_left_is_false__index_is_zero__first_symbol_is_not_merge_or_ignore_merge_symbol():
  symbols = ("a", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  res_1, res_2 = get_next_merged_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, False)

  assert res_1 == "&a"
  assert res_2 == 2


# all except first one useless? Will delete them in test_ipa2symb but they work, can be copypasted there again

def test_get_next_merged_symbol_and_index__from_left_is_false__index_is_zero__first_symbol_is_ignore_merge_symbol():
  symbols = (" ", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  res_1, res_2 = get_next_merged_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, False)

  assert res_1 == " "
  assert res_2 == 1


def test_get_next_merged_symbol_and_index__from_left_is_false__index_is_zero__first_symbol_is_merge_symbol_second_one_is_not():
  symbols = ("&", "a", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  res_1, res_2 = get_next_merged_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, False)

  assert res_1 == "&"
  assert res_2 == 1


def test_get_next_merged_symbol_and_index__from_left_is_false__index_is_zero__first_symbol_is_merge_symbol_second_one_is_too():
  symbols = ("&", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  res_1, res_2 = get_next_merged_symbol_and_index(
    symbols, 0, merge_symbols, ignore_merge_symbols, False)

  assert res_1 == "&"
  assert res_2 == 1

#


def test_get_next_merged_symbol_and_index__from_left_is_false__index_is_last__last_symbol_is_not_merge_or_ignore_merge_symbol():
  symbols = ("a", "&", "bc")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  res_1, res_2 = get_next_merged_symbol_and_index(
    symbols, 2, merge_symbols, ignore_merge_symbols, False)

  assert res_1 == "bc"
  assert res_2 == 3


def test_get_next_merged_symbol_and_index__from_left_is_false__index_is_last__last_symbol_is_ignore_merge_symbol():
  symbols = ("a", "&", " ")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  res_1, res_2 = get_next_merged_symbol_and_index(
    symbols, 2, merge_symbols, ignore_merge_symbols, False)

  assert res_1 == " "
  assert res_2 == 3


def test_get_next_merged_symbol_and_index__from_left_is_false__index_is_last__first_symbol_is_merge_symbol_second_one_is_not():
  symbols = ("a", "bc", "&")
  merge_symbols = {"&"}
  ignore_merge_symbols = {" "}
  res_1, res_2 = get_next_merged_symbol_and_index(
    symbols, 2, merge_symbols, ignore_merge_symbols, False)

  assert res_1 == "&"
  assert res_2 == 3
