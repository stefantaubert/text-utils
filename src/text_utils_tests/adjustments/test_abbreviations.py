from text_utils.adjustments.abbreviations import (
    expand_abbreviations, expand_units_of_measure,
    replace_big_letter_abbreviations)


def test_replace_big_letter_abbreviations():
  res = replace_big_letter_abbreviations("BC BC BCab abBC BC")
  assert res == "B C B C B Cab abB C B C"


def test_expand_abbreviations():
  res = expand_abbreviations(
    "mrs. mr. dr. st. co. jr. maj. gen. drs. rev. lt. hon. sgt. capt. esq. ltd. col. ft. Mrs. mrs gen")
  assert res == "misess mister doctor saint company junior major general doctors reverend lieutenant honorable sergeant captain esquire limited colonel fort misess mrs gen"


def test_expand_units_of_measure():
  res = expand_units_of_measure("g kg mm cm m S s he's min.")
  assert res == "g kilograms millimeters centimeters meters S seconds he's minutes."
