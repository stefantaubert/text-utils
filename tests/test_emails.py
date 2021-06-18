import unittest

from text_utils.adjustments.emails import (replace_at_symbols,
                                           replace_mail_addresses)


class UnitTests(unittest.TestCase):

  def test_replace_mail_addresses_valid_mail(self):
    res = replace_mail_addresses("abc@def.de")
    assert res == "abc at def dot de"

  def test_replace_mail_addresses_invalid_mail_no_dot(self):
    res = replace_mail_addresses("abc@defde")
    assert res == "abc@defde"

  def test_replace_mail_addresses_invalid_mail_no_at(self):
    res = replace_mail_addresses("abcdef.de")
    assert res == "abcdef.de"

  def test_replace_mail_addresses_invalid_mail_no_dot_and_at(self):
    res = replace_mail_addresses("abcdefde")
    assert res == "abcdefde"

  def test_replace_at_symbols_no_space(self):
    res = replace_at_symbols("abc@def")
    assert res == "abc at def"

  def test_replace_at_symbols_l_space(self):
    res = replace_at_symbols("abc @def")
    assert res == "abc at def"

  def test_replace_at_symbols_r_space(self):
    res = replace_at_symbols("abc@ def")
    assert res == "abc at def"

  def test_replace_at_symbols_both_space(self):
    res = replace_at_symbols("abc @ def")
    assert res == "abc at def"

  def test_replace_at_symbols_double_at(self):
    res = replace_at_symbols("abc@@def")
    assert res == "abc at  at def"


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
