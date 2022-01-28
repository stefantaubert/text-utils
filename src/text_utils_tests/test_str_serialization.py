from text_utils.str_serialization import str_deserialization


def test_str_serialization():
  text = "St 1s   3s"
  res = list(str_deserialization(text, " "))

  assert res == ["St", "1s", " ", "3s"]


def test_str_serialization_five_spaces():
  text = "St     5s"
  res = list(str_deserialization(text, " "))

  assert res == ["St", " ", " ", "5s"]


def test_str_serialization_seven_spaces():
  text = "St       7s"
  res = list(str_deserialization(text, " "))

  assert res == ["St", " ", " ", " ", "7s"]


def test_str_serialization_two_spaces_at_end():
  text = "St 1s  "
  res = list(str_deserialization(text, " "))

  assert res == ["St", "1s", " "]
