from text_utils.text_selection.random_applied import *

n_data = 6
data = OrderedDict({i: ["a"] for i in range(n_data)})
durations = {k: 1 for k in data.keys()}

res = get_n_divergent_seconds(
  durations_s=durations,
  seconds=4,
  n=3,
)
