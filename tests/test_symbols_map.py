import os
import tempfile

from text_utils.symbol_id_dict import SymbolIdDict
from text_utils.symbols_map import SymbolsMap, create_or_update_inference_map


def test_from_two_sets():
  m = SymbolsMap.from_intersection({"a", "b"}, {"b", "c"})

  assert len(m) == 2
  assert m["b"] == "b"
  assert m["c"] == ""


def test_update_existing_to_mappings_overwrites_empty_mapping():
  old = SymbolsMap({"a": ""})

  old.update_existing_to_mappings({"a": "a"})

  assert len(old) == 1
  assert old["a"] == "a"


def test_update_existing_to_mappings_ignores_mapping_with_unknown_symbol():
  old = SymbolsMap({"b": ""})

  old.update_existing_to_mappings({"a": "a"})

  assert len(old) == 1
  assert old["b"] == ""


def test_update_existing_to_mappings_ignores_mapping_with_empty_symbol():
  old = SymbolsMap({"a": "a"})

  old.update_existing_to_mappings({"a": ""})

  assert len(old) == 1
  assert old["a"] == "a"

# def test_update_map_non_existing_symbols_are_ignored():
#   old_map = SymbolsMap([
#     ("a", "a"),
#   ])

#   new_map = SymbolsMap([
#     ("b", "b"),
#   ])

#   res = update_map(old_map, new_map)

#   self.assertEqual(1, len(new_map))
#   self.assertEqual("b", new_map["b"])
#   self.assertTrue(res)

# def test_update_map_new_symbols_are_taken():
#   old_map = SymbolsMap([
#     ("a", "a"),
#   ])

#   new_map = SymbolsMap([
#     ("a", "b"),
#   ])

#   res = update_map(old_map, new_map)

#   self.assertEqual(1, len(new_map))
#   self.assertEqual("b", new_map["a"])
#   self.assertFalse(res)

# def test_update_map_new_symbols_are_added():
#   old_map = SymbolsMap([
#     ("a", "a"),
#   ])

#   new_map = SymbolsMap([
#     ("a", "a"),
#     ("b", "b"),
#   ])

#   res = update_map(old_map, new_map)

#   self.assertEqual(2, len(new_map))
#   self.assertEqual("a", new_map["a"])
#   self.assertEqual("b", new_map["b"])
#   self.assertTrue(res)

# def test_update_map():
#   old_map = SymbolsMap([
#     ("a", "a"),
#     ("b", "c"),
#     ("d", ""),
#     ("g", "h"),
#   ])

#   new_map = SymbolsMap([
#     ("a", "c"),
#     ("b", "a"),
#     ("d", "x"),
#     ("e", "f"),
#     ("g", ""),
#   ])

#   res = update_map(old_map, new_map)

#   self.assertEqual("c", new_map["a"])
#   self.assertEqual("a", new_map["b"])
#   self.assertEqual("x", new_map["d"])
#   self.assertEqual("f", new_map["e"])
#   self.assertEqual("h", new_map["g"])
#   self.assertTrue(res)


def test_save_load_symbols_map():
  path = tempfile.mktemp()
  symbols_map = SymbolsMap({
    "b": "a",
    "c": "b",
    "x": "y",
  })
  symbols_map.save(path)
  res = SymbolsMap.load(path)
  os.remove(path)

  assert len(res) == 3
  assert res["b"] == "a"
  assert res["c"] == "b"
  assert res["x"] == "y"


def test_create_or_update_map_no_other_maps():
  orig_symbols = {"b", "c"}
  corpora = {"a", "b"}

  symbols_id_map, symbols = create_or_update_inference_map(
    orig=orig_symbols,
    dest=corpora,
    existing_map=None,
    template_map=None,
  )

  assert symbols_id_map["a"] == ""
  assert symbols_id_map["b"] == "b"
  assert 2 == len(symbols_id_map)
  assert symbols == ["b", "c"]


def test_create_or_update_map_with_template_map():
  orig_symbols = {"c", "d", "e"}
  corpora = {"a", "b", "c"}

  template_map = SymbolsMap({
    "b": "d",
    "e": "f"
  })

  symbols_id_map, symbols = create_or_update_inference_map(
    orig=orig_symbols,
    dest=corpora,
    template_map=template_map,
    existing_map=None,
  )

  assert symbols_id_map["a"] == ""
  assert symbols_id_map["b"] == "d"
  assert symbols_id_map["c"] == "c"
  assert len(symbols_id_map) == 3
  assert symbols == ["c", "d", "e"]


def test_create_or_update_map_with_template_map_and_existing_map():
  orig_symbols = {"c", "d", "e"}
  corpora = {"a", "b", "c"}

  template_map = SymbolsMap({
    "b": "d",
    "e": "f"
  })

  symbols_id_map, symbols = create_or_update_inference_map(
    orig=orig_symbols,
    dest=corpora,
    template_map=template_map,
    existing_map=None,
  )

  assert symbols_id_map["a"] == ""
  assert symbols_id_map["b"] == "d"
  assert symbols_id_map["c"] == "c"
  assert len(symbols_id_map) == 3
  assert symbols == ["c", "d", "e"]


def test_get_symbols_id_mapping_without_map():
  from_symbols = {"b", "c"}
  to_symbols = {"a", "b"}
  from_conv = SymbolIdDict.init_from_symbols(from_symbols)
  to_conv = SymbolIdDict.init_from_symbols(to_symbols)
  mapping = SymbolsMap.from_intersection(from_symbols, to_symbols)
  mapping.update_existing_to_mappings({"a": "c"})

  symbols_id_map = mapping.convert_to_symbols_ids_map(
    to_symbols=to_conv,
    from_symbols=from_conv,
  )

  assert symbols_id_map[from_conv.get_id("b")] == to_conv.get_id("b")
  assert symbols_id_map[from_conv.get_id("c")] == to_conv.get_id("a")
  assert len(symbols_id_map) == 2
