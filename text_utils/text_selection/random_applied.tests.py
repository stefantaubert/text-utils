import random
import unittest

from text_utils.text_selection.random_applied import (get_n_divergent_seconds,
                                                      get_next_start_index)
from text_utils.text_selection.random_export import *
from text_utils.text_selection.utils import *

get_random_seconds_divergence_seeds

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
            'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def get_random_list(length: int, chars: List[str]) -> List[str]:
  res = [random.choice(chars) for _ in range(length)]
  return res


class UnitTests(unittest.TestCase):

  def test_get_right_start_index__expect_index_following_prev_vec(self):
    n_data = 8
    step_length = 4
    durations = OrderedDict({index: 1 for index in range(n_data)})
    prev_vec = [0, 1, 2, 3]
    data_keys = list(range(n_data))

    res = get_next_start_index(
      step_length=step_length,
      durations_s=durations,
      prev_vec=prev_vec,
      data_keys=data_keys
    )

    self.assertTrue(isinstance(res, int))
    self.assertEqual(4, res)

  def test_get_right_start_index__expect_index_following_prev_vec_although_step_length_is_not_reached(self):
    n_data = 8
    step_length = 5
    durations = OrderedDict({index: 1 for index in range(n_data)})
    prev_vec = [0, 1, 2, 3]
    data_keys = list(range(n_data))

    res = get_next_start_index(
      step_length=step_length,
      durations_s=durations,
      prev_vec=prev_vec,
      data_keys=data_keys
    )

    self.assertTrue(isinstance(res, int))
    self.assertEqual(4, res)

  def test_get_right_start_index__dur_sum_will_equal_step_length(self):
    n_data = 8
    step_length = 4
    durations = OrderedDict({index: 2 for index in range(n_data)})
    prev_vec = [0, 1, 2, 3]
    data_keys = list(range(n_data))

    res = get_next_start_index(
      step_length=step_length,
      durations_s=durations,
      prev_vec=prev_vec,
      data_keys=data_keys
    )

    self.assertTrue(isinstance(res, int))
    self.assertEqual(2, res)

  def test_get_right_start_index__dur_sum_will_get_bigger_than_step_length(self):
    n_data = 8
    step_length = 3
    durations = OrderedDict({index: 2 for index in range(n_data)})
    prev_vec = [0, 1, 2, 3]
    data_keys = list(range(n_data))

    res = get_next_start_index(
      step_length=step_length,
      durations_s=durations,
      prev_vec=prev_vec,
      data_keys=data_keys
    )

    self.assertTrue(isinstance(res, int))
    self.assertEqual(2, res)

  def test_get_right_start_index__durs_differ(self):
    step_length = 2
    durations = OrderedDict({
      0: 1,
      1: 7,
      2: 1
    })
    prev_vec = [0, 1, 2]
    data_keys = list(range(3))

    res = get_next_start_index(
      step_length=step_length,
      durations_s=durations,
      prev_vec=prev_vec,
      data_keys=data_keys
    )

    self.assertTrue(isinstance(res, int))
    self.assertEqual(1, res)

  def test_get_n_divergent_seconds__one_iteration(self):
    n_data = 4
    durations = OrderedDict({k: 1 for k in range(n_data)})

    res = get_n_divergent_seconds(
      durations_s=durations,
      seconds=3,
      n=1,
    )

    self.assertEqual(1, len(res))
    self.assertEqual(3, len(res[0]))

  def test_get_n_divergent_seconds__two_iterations__no_overflowing(self):
    n_data = 2
    durations = OrderedDict({k: 1 for k in range(n_data)})

    res = get_n_divergent_seconds(
      durations_s=durations,
      seconds=1,
      n=2,
    )

    self.assertEqual(2, len(res))
    self.assertEqual(1, len(res[0]))
    self.assertEqual(1, len(res[1]))
    self.assertEqual(0, len(set(res[0]).intersection(set(res[1]))))

  def test_get_n_divergent_seconds__two_iterations__with_overflowing_once(self):
    n_data = 3
    durations = OrderedDict({k: 1 for k in range(n_data)})

    res = get_n_divergent_seconds(
      durations_s=durations,
      seconds=2,
      n=2,
    )

    self.assertEqual(2, len(res))
    self.assertEqual(1, len(set(res[0]).intersection(set(res[1]))))

  def test_get_n_divergent_seconds__two_iterations__with_overflowing_twice(self):
    n_data = 6
    durations = OrderedDict({k: 1 for k in range(n_data)})

    res = get_n_divergent_seconds(
      durations_s=durations,
      seconds=4,
      n=3,
    )

    self.assertEqual(3, len(res))
    self.assertEqual(2, len(set(res[0]).intersection(set(res[1]))))
    self.assertEqual(2, len(set(res[1]).intersection(set(res[2]))))
    self.assertEqual(2, len(set(res[0]).intersection(set(res[2]))))

  def test_get_n_divergent_seconds__with_different_durations(self):
    durations = OrderedDict({
      0: 1,
      1: 7,
      2: 1
    })
    res = get_n_divergent_seconds(
      durations_s=durations,
      seconds=7,
      n=3
    )

    self.assertEqual(3, len(res))
    self.assertEqual([0], res[0])
    self.assertEqual([1], res[1])
    self.assertEqual([2, 0], res[2])

  def test_get_n_divergent_seconds__durations_differ__expect_three_times_all_keys_but_first_is_in_different_order(self):
    durations = OrderedDict({
      0: 1,
      1: 7,
      2: 1
    })
    res = get_n_divergent_seconds(
      durations_s=durations,
      seconds=9,
      n=3
    )

    self.assertEqual(3, len(res))
    self.assertEqual([0, 1, 2], res[0])
    self.assertEqual([1, 2, 0], res[1])
    self.assertEqual([1, 2, 0], res[2])

  def test_get_n_divergent_seconds__same_durations__expect_three_times_all_keys_but_all_in_different_order(self):
    durations = OrderedDict({
      0: 1,
      1: 1,
      2: 1
    })
    res = get_n_divergent_seconds(
      durations_s=durations,
      seconds=3,
      n=3
    )

    self.assertEqual(3, len(res))
    self.assertEqual([0, 1, 2], res[0])
    self.assertEqual([1, 2, 0], res[1])
    self.assertEqual([2, 0, 1], res[2])

  def test_get_n_divergent_seconds__with_many_different_durations(self):
    durations = OrderedDict({
      0: 1,
      1: 2,
      2: 3,
      3: 1,
      4: 1,
      5: 2,
      6: 2
    })

    res = get_n_divergent_seconds(
      durations_s=durations,
      seconds=7,
      n=3,
    )

    self.assertEqual(3, len(res))
    self.assertEqual([0, 1, 2, 3], res[0])
    self.assertEqual([2, 3, 4, 5], res[1])
    self.assertEqual([5, 6, 0, 1], res[2])

  def test_get_random_seconds_divergence_seeds(self):
    seed = 1111
    random.seed(seed)

    n_data = 10000
    data = OrderedDict({i: get_random_list(random.randint(1, 50), ALPHABET) for i in range(n_data)})

    durations = OrderedDict({k: random.randint(1, 10) for k in data.keys()})

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
