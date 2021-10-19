import random

import numpy as np
from text_utils.text_selection.utils import *

N = 500  # 0  # Anzahl Sets aus denen gewählt wird
l = 1000  # 0  # max id
x = 450  # 0  # so viele Einträge soll jedes Set ca haben
n = 5  # so viele Sets sollen letztendlcih ausgewählt werden

RANGE = list(range(l))

sample_set_list = []
for i in range(N):
  #set_length = x + random.randint(-100,101)
  # random.seed = 5 * i**3 - 2 * i**2 + 3 * i -7 2
  random.shuffle(RANGE)
  random_set = set(RANGE[:x])
  sample_set_list.append(random_set)

cluster_chosen_indices = find_unlike_sets(sample_set_list, n, 1111)
cluster_chosen_sets = get_chosen_sets(sample_set_list, cluster_chosen_indices)
print(get_total_number_of_common_elements(cluster_chosen_sets))
print("...")

random_scores = []
for i in range(1000):
  random_chosen_indices = get_random_subset_indices(sample_set_list, n)
  random_chosen_sets = get_chosen_sets(sample_set_list, random_chosen_indices)
  random_scores.append(get_total_number_of_common_elements(random_chosen_sets))

print(np.mean(random_scores))
# print("ljglejrtg")
