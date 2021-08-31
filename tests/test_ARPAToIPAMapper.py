from text_utils.ARPAToIPAMapper import get_ipa_with_stress


def test_UH():
  inp = "UH"
  res = get_ipa_with_stress(inp)
  assert res == "ʊ"


def test_UH0():
  inp = "UH0"
  res = get_ipa_with_stress(inp)

  assert res == "ʊ"


def test_UH1():
  inp = "UH1"
  res = get_ipa_with_stress(inp)

  assert res == "ˈʊ"


def test_UH2():
  inp = "UH2"
  res = get_ipa_with_stress(inp)

  assert res == "ˌʊ"
