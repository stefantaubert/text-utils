from text_utils.symbol_id_dict import SymbolIdDict


def test_remove_symbol_ids():
  res = SymbolIdDict.init_from_symbols({"a", "b", "c"})

  res.remove_ids({0, 2})
  assert len(res) == 1
  assert res.get_symbol(1) == "b"
  assert res.get_id("b") == 1


def test_init_from_symbols_adds_no_symbols():
  res = SymbolIdDict.init_from_symbols({"a", "b", "c"})

  assert len(res) == 3


def test_init_from_symbols_is_sorted():
  res = SymbolIdDict.init_from_symbols({"c", "a", "b"})

  assert res.get_symbol(0) == "a"
  assert res.get_symbol(1) == "b"
  assert res.get_symbol(2) == "c"


def test_get_text_from_serialized_ids():
  symbol_ids = SymbolIdDict.init_from_symbols({"a", "b"})

  res = symbol_ids.get_text("0,1,1")

  assert res == "abb"


def test_get_text_from_ids():
  symbol_ids = SymbolIdDict.init_from_symbols({"a", "b"})

  res = symbol_ids.get_text((0, 1, 1))

  assert res == "abb"


def test_init_from_symbols_with_pad_has_pad_at_idx_zero():
  res = SymbolIdDict.init_from_symbols_with_pad({"b", "a"}, "xx")

  assert res.get_symbol(0) == "xx"
  assert res.get_symbol(1) == "a"
  assert res.get_symbol(2) == "b"


def test_init_from_symbols_with_pad_ignores_existing_pad():
  res = SymbolIdDict.init_from_symbols_with_pad({"b", "a", "xx"}, "xx")

  assert res.get_symbol(0) == "xx"
  assert res.get_symbol(1) == "a"
  assert res.get_symbol(2) == "b"
