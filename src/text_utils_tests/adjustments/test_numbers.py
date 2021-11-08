from text_utils.adjustments.numbers import (__replace_e_to_the_power_of,
                                            __replace_minus, normalize_numbers)


def test_replace_e_to_the_power_of__e_minus():
  res = __replace_e_to_the_power_of("e-5654")
  assert res == "ten to the power of minus 5654"


def test_replace_e_to_the_power_of__e_no_minus():
  res = __replace_e_to_the_power_of("e5654")
  assert res == "ten to the power of 5654"


def test_replace_e_to_the_power_of__prefix_e_no_minus():
  res = __replace_e_to_the_power_of("45e5654")
  assert res == "45 times ten to the power of 5654"


def test_replace_e_to_the_power_of__prefix_e_minus():
  res = __replace_e_to_the_power_of("45e-5654")
  assert res == "45 times ten to the power of minus 5654"


def test_replace_minus__normal():
  res = __replace_minus("-5654")
  assert res == "minus 5654"


def test_replace_minus__with_e__no_replacement():
  res = __replace_minus("e-5654")
  assert res == "e-5654"


def test_replace_minus__on_begin__replacement():
  res = __replace_minus("-5654")
  assert res == "minus 5654"


def test_replace_minus__with_space__replacement():
  res = __replace_minus(" -5654")
  assert res == " minus 5654"


def test_normalize_numbers():
  res = normalize_numbers("$5654 -54 5e-21 test $300,000.40")
  assert res == "five thousand, six hundred fifty-four dollars minus fifty-four five times ten to the power of minus twenty-one test three hundred thousand dollars, forty cents"


def test_expand_number():
  pass
