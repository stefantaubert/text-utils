import unittest

from text_utils.text_selection.random_export import *
from text_utils.text_selection.utils import *


class UnitTests(unittest.TestCase):
  def test_random_default__returns_random(self):
    data = OrderedDict({
      1: ["a", "a"],  # one new
      2: ["c", "a"],  # two new
      3: ["d", "a"],  # two new
    })

    res = random_default(
      data=data,
      seed=1,
    )

    assert_res = OrderedSet([2, 3, 1])
    self.assertEqual(assert_res, res)

  def test_random_ngrams_default_cover__returns_covered_random(self):
    data = OrderedDict({
      1: ["a"],
      2: ["a"],
      3: ["c"],
      4: ["a"],
      5: ["d"],
    })

    seed_tries = range(500)

    for seed in seed_tries:
      res = random_ngrams_cover_default(
        data=data,
        seed=seed,
        ignore_symbols=None,
        n_gram=1,
      )

      entries = [data[x][0] for x in res]

      self.assertEqual({"a", "c", "d"}, set(entries[:3]))
      self.assertEqual(5, len(res))


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
