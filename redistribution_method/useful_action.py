def useful_action(cost_matrix: list[list[int]], sparse_matrix: list[list[int]], item_cors: list[int]):
    cost_item = cost_matrix[item_cors[0]][item_cors[1]]

    for item_index in range(len(sparse_matrix)):
        sparse_matrix[item_index][item_cors[1]] -= cost_item

    return sparse_matrix
