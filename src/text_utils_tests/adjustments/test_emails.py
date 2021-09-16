from text_utils.adjustments.emails import (replace_at_symbols,
                                           replace_mail_addresses)


def test_replace_mail_addresses_valid_mail():
  res = replace_mail_addresses("abc@def.de")
  assert res == "abc at def dot de"


def test_replace_mail_addresses_invalid_mail_no_dot():
  res = replace_mail_addresses("abc@defde")
  assert res == "abc@defde"


def test_replace_mail_addresses_invalid_mail_no_at():
  res = replace_mail_addresses("abcdef.de")
  assert res == "abcdef.de"


def test_replace_mail_addresses_invalid_mail_no_dot_and_at():
  res = replace_mail_addresses("abcdefde")
  assert res == "abcdefde"


def test_replace_at_symbols_no_space():
  res = replace_at_symbols("abc@def")
  assert res == "abc at def"


def test_replace_at_symbols_l_space():
  res = replace_at_symbols("abc @def")
  assert res == "abc at def"


def test_replace_at_symbols_r_space():
  res = replace_at_symbols("abc@ def")
  assert res == "abc at def"


def test_replace_at_symbols_both_space():
  res = replace_at_symbols("abc @ def")
  assert res == "abc at def"


def test_replace_at_symbols_double_at():
  res = replace_at_symbols("abc@@def")
  assert res == "abc at  at def"
