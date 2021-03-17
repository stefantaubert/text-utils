import unittest

from text_utils.text_selection.greedy_export import *
from text_utils.text_selection.utils import *


class UnitTests(unittest.TestCase):
  def test_greedy_ngrams_iterations__one_grams__return_correct_sorting(self):
    data = OrderedDict({
      1: ["a", "a"],  # one new
      2: ["c", "a"],  # two new
      3: ["d", "a"],  # two new
    })

    res = greedy_ngrams_iterations(
      data=data,
      n_gram=1,
      ignore_symbols=None,
      iterations=3,
    )

    assert_res = OrderedSet([2, 3, 1])
    self.assertEqual(assert_res, res)

  def test_greedy_ngrams_epochs__one_grams_one_epoch__return_correct_sorting(self):
    data = OrderedDict({
      1: ["a", "a"],  # one new
      2: ["c", "a"],  # two new
      3: ["d", "a"],  # two new
    })

    res = greedy_ngrams_epochs(
      data=data,
      n_gram=1,
      ignore_symbols=None,
      epochs=1,
    )

    assert_res = OrderedSet([2, 3])
    self.assertEqual(assert_res, res)

  def test_greedy_ngrams_seconds__one_gram_two_seconds__return_correct_sorting(self):
    data = OrderedDict({
      1: ["a", "a"],  # one new
      2: ["c", "a"],  # two new
      3: ["d", "a"],  # two new
    })

    durations = {
      1: 1,
      2: 1,
      3: 1,
    }

    res = greedy_ngrams_seconds(
      data=data,
      n_gram=1,
      ignore_symbols=None,
      durations_s=durations,
      seconds=2,
    )

    assert_res = OrderedSet([2, 3])
    self.assertEqual(assert_res, res)

  def test_greedy_ngrams_cound__one_gram_two_counts__return_correct_sorting(self):
    data = OrderedDict({
      1: ["a", "a"],  # one new
      2: ["c", "a"],  # two new
      3: ["d", "a"],  # two new
    })

    counts = {
      1: 1,
      2: 1,
      3: 1,
    }

    res = greedy_ngrams_count(
      data=data,
      n_gram=1,
      ignore_symbols=None,
      chars=counts,
      total_count=2,
    )

    assert_res = OrderedSet([2, 3])
    self.assertEqual(assert_res, res)


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
