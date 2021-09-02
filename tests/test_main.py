from text_utils.pronunciation.main import merge_symbols


def test_merge_symbols__no_merge_symbols():
  res = merge_symbols(
    pronunciation=("a", " ", "b",),
    merge_at=" ",
    merge_symbols={},
  )

  assert res == ("a", " ", "b",)


def test_merge_symbols__empty_pron():
  res = merge_symbols(
    pronunciation=tuple(),
    merge_at=" ",
    merge_symbols={},
  )

  assert res == tuple()


def test_merge_symbols__no_merge_at__only_merge_symbols__merges():
  res = merge_symbols(
    pronunciation=("?", "!"),
    merge_at=" ",
    merge_symbols={"?", "!"},
  )

  assert res == ("?!",)


def test_merge_symbols__no_merge_at__merges():
  res = merge_symbols(
    pronunciation=("?", "b", "!"),
    merge_at=" ",
    merge_symbols={"?", "!"},
  )

  assert res == ("?b!",)


def test_merge_symbols__merge_to_previous_symbol():
  res = merge_symbols(
    pronunciation=("a", " ", "b", "!"),
    merge_at=" ",
    merge_symbols={"!"},
  )

  assert res == ("a", " ", "b!",)


def test_merge_symbols__dont_merge_if_no_symbol_to_merge():
  res = merge_symbols(
    pronunciation=("a", " ", "!",),
    merge_at=" ",
    merge_symbols={"!"},
  )

  assert res == ("a", " ", "!",)
