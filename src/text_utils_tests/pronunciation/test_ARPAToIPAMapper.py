from text_utils.pronunciation.ARPAToIPAMapper import (
    get_ipa_mapping_with_stress, has_ipa_mapping, symbol_map_arpa_to_ipa,
    symbols_map_arpa_to_ipa)


def test_UH():
  inp = "UH"
  res = get_ipa_mapping_with_stress(inp)
  assert res == "ʊ"


def test_UH0():
  inp = "UH0"
  res = get_ipa_mapping_with_stress(inp)

  assert res == "ʊ"


def test_UH1():
  inp = "UH1"
  res = get_ipa_mapping_with_stress(inp)

  assert res == "ˈʊ"


def test_UH2():
  inp = "UH2"
  res = get_ipa_mapping_with_stress(inp)

  assert res == "ˌʊ"


def test_has_ipa_mapping__valid_symbol_no_stress__is_true():
  result = has_ipa_mapping("UH")
  assert result


def test_has_ipa_mapping__valid_symbol_zero_stress__is_true():
  result = has_ipa_mapping("UH0")
  assert result


def test_has_ipa_mapping__valid_symbol_primary_stress__is_true():
  result = has_ipa_mapping("UH1")
  assert result


def test_has_ipa_mapping__valid_symbol_secondary_stress__is_true():
  result = has_ipa_mapping("UH2")
  assert result


def test_has_ipa_mapping__valid_symbol_double_secondary_stress__is_false():
  result = has_ipa_mapping("UH22")
  assert not result


def test_has_ipa_mapping__not_valid_entry():
  result = has_ipa_mapping("ABC")
  assert not result


def test_has_ipa_mapping__not_valid_entry_with_stress():
  result = has_ipa_mapping("ABC1")
  assert not result


def test_map_arpa_to_ipa_component_test():
  sentence = ('DH', 'IH0', 'S', ' ', 'IH0', 'Z', ' ', 'AH0', ' ', 'T', 'EH1', 'S', 'T', ".",)

  result = symbols_map_arpa_to_ipa(
    arpa_symbols=sentence,
    ignore={},
    replace_unknown=False,
    replace_unknown_with=None,
  )

  assert result == ('ð', 'ɪ', 's', ' ', 'ɪ', 'z', ' ', 'ʌ', ' ', 't', 'ˈɛ', 's', 't', '.',)


def test_map_arpa_to_ipa__multitest():
  result = symbols_map_arpa_to_ipa(
    arpa_symbols=("UH1", "UH2", "ABC", "DEF",),
    ignore={"ABC", "UH2"},
    replace_unknown=True,
    replace_unknown_with="<unk>",
  )

  assert result == ("ˈʊ", "UH2", "ABC", "<unk>",)


def test_symbol_map_arpa_to_ipa__valid_arpa():
  result = symbol_map_arpa_to_ipa(
    arpa_symbol="UH1",
    ignore={},
    replace_unknown=False,
    replace_unknown_with=None,
  )

  assert result == "ˈʊ"


def test_symbol_map_arpa_to_ipa__valid_arpa_ignore__is_ignored():
  result = symbol_map_arpa_to_ipa(
    arpa_symbol="UH1",
    ignore={"UH1"},
    replace_unknown=False,
    replace_unknown_with=None,
  )

  assert result == "UH1"


def test_symbol_map_arpa_to_ipa__replace_unknown_has_value():
  result = symbol_map_arpa_to_ipa(
    arpa_symbol="DEF",
    ignore={},
    replace_unknown=True,
    replace_unknown_with="<unk>",
  )

  assert result == "<unk>"


def test_symbol_map_arpa_to_ipa__replace_unknown_is_empty():
  result = symbol_map_arpa_to_ipa(
    arpa_symbol="DEF",
    ignore={},
    replace_unknown=True,
    replace_unknown_with="",
  )

  assert result is None


def test_symbol_map_arpa_to_ipa__replace_unknown_is_None():
  result = symbol_map_arpa_to_ipa(
    arpa_symbol="DEF",
    ignore={},
    replace_unknown=True,
    replace_unknown_with=None,
  )

  assert result is None
