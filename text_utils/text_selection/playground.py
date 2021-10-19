def find_unlike_sets(sample_set_list: List[Set[int]], n: int, seed: Optional[int]) -> List[int]:
  k_means = KMeans(
    n_clusters=n,
    init='k-means++',
    random_state=seed,
  )

  max_id = get_max_entry(sample_set_list)
  vecs = vectorize_all_sets(sample_set_list, max_id)
  cluster_dists = k_means.fit_transform(vecs)
  cluster_labels = k_means.labels_
  for cluster_index in range(n):
    cluster_is_not_empty_for_this_index = any(cluster_labels == cluster_index)
    assert cluster_is_not_empty_for_this_index
  assert cluster_dists.shape[1] == n
  chosen_indices = np.argmin(cluster_dists, axis=0)
  for i in range(n):
    while cluster_labels[chosen_indices[i]] != i:
      cluster_dists[chosen_indices[i], i] = inf
      chosen_indices[i] = np.argmin(cluster_dists[:, i])

  chosen_sets = [sample_set_list[i] for i in range(len(sample_set_list)) if i in chosen_indices]
  random_chosen = get_random_subsets(sample_set_list, n)
  print("Total number of common elements in subset with clustering method:",
        get_total_number_of_common_elements(chosen_sets))
  print("Total number of common elements in subset with random method:",
        get_total_number_of_common_elements(random_chosen))

  # c = k_means.fit(vecs)
  # d = c.labels_
  # pca = PCA(2)
  # p = pca.fit_transform(vecs)
  # color_list = ["green", "blue", "yellow", "black", "red"]
  # for i in range(n):
  #   filtered_labels = p[d == i]
  #   plt.scatter(filtered_labels[:, 0], filtered_labels[:, 1], color=color_list[i])
  # # filter rows of original data
  # # filtered_label0 = p[d == 0]
  # # filtered_label1 = p[d == 1]
  # # # Plotting the results
  # # plt.scatter(filtered_label0[:, 0], filtered_label0[:, 1], color='red')
  # # plt.scatter(filtered_label1[:, 0], filtered_label1[:, 1], color='black')
  # plt.show()
  # plt.savefig("verfickterplot.png")

  assert len(chosen_indices) == n
  assert len(set(chosen_indices)) == n
  return chosen_indices  # als ordered set
  # falls len(set) < n ...
  #chosen_sets = [sample_set_list[i] for i in range(len(sample_set_list)) if i in chosen_indices]
