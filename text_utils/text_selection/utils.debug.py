import random
from typing import Dict, List, Set

from text_utils.text_selection.utils import *


def get_random_subset_indices(sample_set_list: List[Set[int]], n: int) -> List[Set[int]]:
  chosen_indices = random.sample(range(len(sample_set_list)), n)
  while len(set(chosen_indices)) != n:
    chosen_indices = random.sample(range(len(sample_set_list)), n)
  chosen_sets = [sample_set_list[i] for i in range(len(sample_set_list)) if i in chosen_indices]
  return chosen_sets


def get_total_number_of_common_elements(chosen_sets: List[Set[int]]) -> int:
  common_elements_dict = get_number_of_common_elements(chosen_sets)
  total_number = sum(common_elements_dict.values()) / 2
  return int(total_number)


def get_number_of_common_elements(chosen_sets: List[Set]) -> Dict[int, int]:
  dict_of_common_elements = {index: sum(list_of_numbers_of_common_elements_for_one_index(
    chosen_sets, index)) for index in range(len(chosen_sets))}
  return dict_of_common_elements


def get_number_of_common_elements_per_set(chosen_sets: List[Set]) -> Dict[int, List[int]]:
  dict_of_common_elements = {index: list_of_numbers_of_common_elements_for_one_index(
    chosen_sets, index) for index in range(len(chosen_sets))}
  return dict_of_common_elements


def list_of_numbers_of_common_elements_for_one_index(chosen_sets: List[Set], index: int) -> List[int]:
  common_number_list = [len(chosen_sets[index] & chosen_set)
                        for chosen_set in chosen_sets if chosen_set != chosen_sets[index]]
  return common_number_list


NUMBER_OF_SETS = 500
NUMBER_OF_RUNS = 20
for j in range(NUMBER_OF_RUNS):
  set_list = []
  for i in range(NUMBER_OF_SETS):
    no_of_elements = random.sample(range(5, 15), 1)
    new_set = set(random.sample(range(1, 100), no_of_elements[0]))
    set_list.append(new_set)
  chosen = find_unlike_sets(set_list, 10, 1)
  random_chosen = get_random_subset_indices(set_list, 10)
  print("Total number of common elements in subset with clustering method:",
        get_total_number_of_common_elements(chosen))
  print("Total number of common elements in subset with random method:",
        get_total_number_of_common_elements(random_chosen))
  print("___________")
