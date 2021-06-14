from text_utils.accents_dict import AccentsDict


def test_init_from_accents_adds_no_accents():
  res = AccentsDict.init_from_accents({"a", "b", "c"})
  assert len(res) == 3


def test_init_from_accents_is_sorted():
  res = AccentsDict.init_from_accents({"c", "a", "b"})

  assert res.get_accent(0) == "a"
  assert res.get_accent(1) == "b"
  assert res.get_accent(2) == "c"


def test_init_from_accents_with_pad_uses_pad_const():
  res = AccentsDict.init_from_accents_with_pad({"b", "a"}, pad_accent="_")

  assert res.get_accent(0) == "_"
  assert res.get_accent(1) == "a"
  assert res.get_accent(2) == "b"


def test_init_from_accents_with_pad_has_pad_at_idx_zero():
  res = AccentsDict.init_from_accents_with_pad({"b", "a"}, "xx")

  assert res.get_accent(0) == "xx"
  assert res.get_accent(1) == "a"
  assert res.get_accent(2) == "b"


def test_init_from_accents_with_pad_ignores_existing_pad():
  res = AccentsDict.init_from_accents_with_pad({"b", "a", "xx"}, "xx")

  assert res.get_accent(0) == "xx"
  assert res.get_accent(1) == "a"
  assert res.get_accent(2) == "b"
