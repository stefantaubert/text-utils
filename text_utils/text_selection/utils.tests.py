import unittest

from text_utils.text_selection.utils import *


class UnitTests(unittest.TestCase):

  def test_get_first_percent_20percent(self):
    data = OrderedSet([1, 2, 3, 4, 5])

    res = get_first_percent(data, 20)

    self.assertEqual(OrderedSet([1]), res)

  def test_get_first_percent_50percent__rounds_up(self):
    data = OrderedSet([1, 2, 3, 4, 5, 6, 7])

    res = get_first_percent(data, 50)

    self.assertEqual(OrderedSet([1, 2, 3, 4]), res)

  def test_get_first_percent_100percent__adds_all(self):
    data = OrderedSet([1, 2, 3, 4, 5, 6, 7])

    res = get_first_percent(data, 100)

    self.assertEqual(OrderedSet([1, 2, 3, 4, 5, 6, 7]), res)

  def test_get_filtered_ngrams__returns_ordered_dict(self):
    data = OrderedDict({
      1: ["a", "b"],
      3: ["e", "f"],
      2: ["c", "d"],
      5: ["i", "j"],
      4: ["g", "h"],
    })

    res = get_filtered_ngrams(
      data=data,
      ignore_symbols=None,
      n_gram=1,
    )

    self.assertTrue(isinstance(res, OrderedDict))

  def test_get_filtered_ngrams__order_is_retained(self):
    data = OrderedDict({
      1: ["a", "b"],
      3: ["e", "f"],
      2: ["c", "d"],
      5: ["i", "j"],
      4: ["g", "h"],
    })

    res = get_filtered_ngrams(
      data=data,
      ignore_symbols=None,
      n_gram=1,
    )

    assert_res = OrderedDict({
      1: [("a",), ("b",)],
      3: [("e",), ("f",)],
      2: [("c",), ("d",)],
      5: [("i",), ("j",)],
      4: [("g",), ("h",)],
    })

    self.assertEqual(assert_res, res)

  def test_get_filtered_ngrams__one_grams__return_one_grams(self):
    data = OrderedDict({
      1: ["a", "b"],
      2: ["c", "a"],
    })

    res = get_filtered_ngrams(
      data=data,
      ignore_symbols=None,
      n_gram=1,
    )

    assert_res = OrderedDict({
      1: [("a",), ("b",)],
      2: [("c",), ("a",)],
    })

    self.assertEqual(assert_res, res)

  def test_get_filtered_ngrams__two_grams__return_two_grams(self):
    data = OrderedDict({
      1: ["a", "b"],
      2: ["c", "a"],
    })

    res = get_filtered_ngrams(
      data=data,
      ignore_symbols=None,
      n_gram=2,
    )

    assert_res = OrderedDict({
      1: [("a", "b",)],
      2: [("c", "a",)],
    })

    self.assertEqual(assert_res, res)

  def test_get_filtered_ngrams__three_grams__return_three_grams(self):
    data = OrderedDict({
      1: ["a", "b", "x"],
      2: ["c", "a", "y"],
    })

    res = get_filtered_ngrams(
      data=data,
      ignore_symbols=None,
      n_gram=3,
    )

    assert_res = OrderedDict({
      1: [("a", "b", "x")],
      2: [("c", "a", "y")],
    })

    self.assertEqual(assert_res, res)

  def test_get_filtered_ngrams__one_grams_filtered__return_filtered_one_grams(self):
    data = OrderedDict({
      1: ["a", "b"],
      2: ["c", "a"],
    })

    res = get_filtered_ngrams(
      data=data,
      ignore_symbols={"a"},
      n_gram=1,
    )

    assert_res = OrderedDict({
      1: [("b",)],
      2: [("c",)],
    })

    self.assertEqual(assert_res, res)

  def test_get_filtered_ngrams__two_grams_filtered__return_filtered_two_grams(self):
    data = OrderedDict({
      1: ["a", "b"],
      2: ["c", "a"],
    })

    res = get_filtered_ngrams(
      data=data,
      ignore_symbols={"b"},
      n_gram=2,
    )

    assert_res = OrderedDict({
      1: [],
      2: [("c", "a",)],
    })

    self.assertEqual(assert_res, res)

  def test_get_filtered_ngrams__three_grams_filtered__return_filtered_three_grams(self):
    data = OrderedDict({
      1: ["a", "b", "x"],
      2: ["c", "a", "y"],
    })

    res = get_filtered_ngrams(
      data=data,
      ignore_symbols={"x"},
      n_gram=3,
    )

    assert_res = OrderedDict({
      1: [],
      2: [("c", "a", "y")],
    })

    self.assertEqual(assert_res, res)

  def test_get_filtered_ngrams__non_existing_ignored__are_ignored(self):
    data = OrderedDict({
      1: ["a", "b"],
      2: ["c", "a"],
    })

    res = get_filtered_ngrams(
      data=data,
      ignore_symbols={"x"},
      n_gram=1,
    )

    assert_res = OrderedDict({
      1: [("a",), ("b",)],
      2: [("c",), ("a",)],
    })

    self.assertEqual(assert_res, res)

  def test_get_filtered_ngrams__empty_list__do_nothing(self):
    data = OrderedDict({
      1: [],
      2: [],
    })

    res = get_filtered_ngrams(
      data=data,
      ignore_symbols=None,
      n_gram=1,
    )

    assert_res = OrderedDict({
      1: [],
      2: [],
    })

    self.assertEqual(assert_res, res)


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
