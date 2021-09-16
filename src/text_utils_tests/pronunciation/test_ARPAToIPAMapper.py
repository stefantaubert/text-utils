from text_utils.pronunciation.arpa_symbols import ALL_ARPA_INCL_STRESSES
from text_utils.pronunciation.ARPAToIPAMapper import (__ARPABET_IPA_MAP,
                                                      symbol_map_arpa_to_ipa,
                                                      symbols_map_arpa_to_ipa)


def test_all_arpa_symbols_are_mapped():
  assert __ARPABET_IPA_MAP.keys() == ALL_ARPA_INCL_STRESSES


def test_UH():
  assert __ARPABET_IPA_MAP["UH"] == "ʊ"


def test_UH0():
  assert __ARPABET_IPA_MAP["UH0"] == "ʊ"


def test_UH1():
  assert __ARPABET_IPA_MAP["UH1"] == "ˈʊ"


def test_UH2():
  assert __ARPABET_IPA_MAP["UH2"] == "ˌʊ"


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
