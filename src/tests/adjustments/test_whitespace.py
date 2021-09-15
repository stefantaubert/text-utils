from text_utils.adjustments.whitespace import collapse_whitespace


def test_collapse_whitespace():
  res = collapse_whitespace("test  a b   c d  e \n  f")
  assert res == "test a b c d e f"
