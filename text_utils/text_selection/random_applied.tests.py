import random
import unittest

from text_utils.text_selection.random_applied import \
    get_n_divergent_random_seconds
from text_utils.text_selection.random_export import *
from text_utils.text_selection.utils import *

get_random_seconds_divergence_seeds

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
            'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def get_random_list(length: int, chars: List[str]) -> List[str]:
  res = [random.choice(chars) for _ in range(length)]
  return res


class UnitTests(unittest.TestCase):
  def test_get_n_divergent_random_seconds__one_iteration(self):
    seed = 1111
    n_data = 8
    data = OrderedDict({i: ["a"] for i in range(n_data)})
    durations = {k: 1 for k in data.keys()}

    res = get_n_divergent_random_seconds(
      durations_s=durations,
      seconds=6,
      n=1,
    )

    self.assertEqual(1, len(res))
    self.assertEqual(6, len(res[0]))

  def test_get_n_divergent_random_seconds__two_iterations__no_overflowing(self):
    seed = 1111
    n_data = 8
    data = OrderedDict({i: ["a"] for i in range(n_data)})
    durations = {k: 1 for k in data.keys()}

    res = get_n_divergent_random_seconds(
      durations_s=durations,
      seconds=4,
      n=2,
    )

    self.assertEqual(2, len(res))
    self.assertEqual(4, len(res[0]))
    self.assertEqual(4, len(res[1]))
    self.assertEqual(0, len(set(res[0]).intersection(set(res[1]))))

  def test_get_n_divergent_random_seconds__two_iterations__with_overflowing_once(self):
    seed = 1111
    n_data = 6
    data = OrderedDict({i: ["a"] for i in range(n_data)})
    durations = {k: 1 for k in data.keys()}

    res = get_n_divergent_random_seconds(
      durations_s=durations,
      seconds=4,
      n=2,
    )

    self.assertEqual(2, len(res))
    self.assertEqual(4, len(res[0]))
    self.assertEqual(4, len(res[1]))
    self.assertEqual(2, len(set(res[0]).intersection(set(res[1]))))

  def test_get_n_divergent_random_seconds__two_iterations__with_overflowing_twice(self):
    seed = 1111
    n_data = 6
    data = OrderedDict({i: ["a"] for i in range(n_data)})
    durations = {k: 1 for k in data.keys()}

    res = get_n_divergent_random_seconds(
      durations_s=durations,
      seconds=4,
      n=3,
    )

    self.assertEqual(3, len(res))
    self.assertEqual(4, len(res[0]))
    self.assertEqual(4, len(res[1]))
    self.assertEqual(4, len(res[2]))
    self.assertEqual(2, len(set(res[0]).intersection(set(res[1]))))
    self.assertEqual(2, len(set(res[1]).intersection(set(res[2]))))
    self.assertEqual(2, len(set(res[0]).intersection(set(res[2]))))

  def test_n_divergent_random_seconds__with_different_durations(self):
    n_data = 7
    data = OrderedDict({i: ["a"] for i in range(n_data)})
    durations = {0: 1, 1: 2, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2}

    res = get_n_divergent_random_seconds(
      durations_s=durations,
      seconds=7,
      n=3,
    )

    self.assertEqual(3, len(res))
    #self.assertEqual(4, len(res[0]))
    #self.assertEqual(4, len(res[1]))
    #self.assertEqual(5, len(res[2]))
    self.assertEqual([0, 1, 2, 3], res[0])
    self.assertEqual([2, 3, 4, 5], res[1])
    self.assertEqual([3, 4, 5, 6, 0], res[2])
    #self.assertEqual(2, len(set(res[0]).intersection(set(res[1]))))
    #self.assertEqual(2, len(set(res[1]).intersection(set(res[2]))))
    #self.assertEqual(2, len(set(res[0]).intersection(set(res[2]))))

  def xtest_get_random_seconds_divergence_seeds(self):
    seed = 1111
    random.seed(seed)

    n_data = 10000
    data = OrderedDict({i: get_random_list(random.randint(1, 50), ALPHABET) for i in range(n_data)})

    durations = {k: random.randint(1, 10) for k in data.keys()}

    res, sets = get_random_seconds_divergence_seeds(
      data=data,
      durations_s=durations,
      seconds=60 * 60,
      seed=seed,
      samples=3000,
      n=2,
    )

    self.assertEqual(OrderedDict({2781, 135}), res)
    self.assertEqual(2, len(sets))


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)
