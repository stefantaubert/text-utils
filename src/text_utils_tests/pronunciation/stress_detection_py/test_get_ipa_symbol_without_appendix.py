from text_utils.pronunciation.ipa_symbols import APPENDIX
from text_utils.pronunciation.stress_detection import \
    get_ipa_symbol_without_appendix


def test_empty__returns_empty():
  result = get_ipa_symbol_without_appendix("")
  assert result == ""


def test_two_symbols_i_and_long__returns_i():
  result = get_ipa_symbol_without_appendix("iː")
  assert result == "i"


def test_combined_symbol_syllabic_n__returns_n():
  result = get_ipa_symbol_without_appendix("n̩")
  assert result == "n"


def test_combined_symbol_i_multiple_tones__returns_i():
  result = get_ipa_symbol_without_appendix("i˥˦˧")
  assert result == "i"


def test_i_primary_stress__returns_unchanged():
  result = get_ipa_symbol_without_appendix("iˈ")
  assert result == "iˈ"


def test_primary_stress_i__returns_unchanged():
  result = get_ipa_symbol_without_appendix("ˈi")
  assert result == "ˈi"


def test_ties_are_not_included__f_tie_above__returns_unchanged():
  result = get_ipa_symbol_without_appendix("f\u0361")
  assert result == "f\u0361"


def test_all_appendix__is_stripped_at_end():
  for appendix in APPENDIX:
    result = get_ipa_symbol_without_appendix("i" + appendix)
    assert result == "i"


def test_all_appendix__is_not_stripped_at_start():
  for appendix in APPENDIX:
    result = get_ipa_symbol_without_appendix(appendix + "i")
    assert result == appendix + "i"
