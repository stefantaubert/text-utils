import pickle
import unittest

from text_utils.text_selection.utils import *


class UnitTests(unittest.TestCase):

  def __init__(self, methodName: str) -> None:
    super().__init__(methodName)

  def test_fail(self):
    with open("/tmp/data.pkl", "rb") as f:
      data = pickle.load(f)

    selected_set_idxs = find_unlike_sets(data, n=2, seed=1111)
    self.assertEqual(2, len(set(selected_set_idxs)))

  def test_find_unlike_sets__same_sets__choose_different_idxs(self):
    data = [set(range(10)) for _ in range(10)]

    selected_set_idxs = find_unlike_sets(data, n=2, seed=1111)
    self.assertEqual(2, len(set(selected_set_idxs)))

  def test_vectorize_all_sets(self):
    sample_set_list = [{1, 4, 5}, {1, 4, 6}]
    max_id = 6
    res = vectorize_all_sets(sample_set_list, max_id)

    self.assertTrue(np.array_equal(res, np.array([[0, 1, 0, 0, 1, 1, 0], [0, 1, 0, 0, 1, 0, 1]])))

  def test_get_max_entry(self):
    sample_set_list = [{1, 4, 5}, {1, 4, 6}]
    res = get_max_entry(sample_set_list)

    self.assertEqual(res, 6)

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
