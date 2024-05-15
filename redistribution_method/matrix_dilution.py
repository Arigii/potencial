def matrix_dilution(cost_matrix: list[list[int]]) -> list[list[int]]:
    sparse_matrix = []

    for row in cost_matrix:
        min_unit = min(row)
        sparse_matrix.append([item - min_unit for item in row])

    for column_index in range(len(sparse_matrix[0])):
        min_unit = min([item[column_index] for item in sparse_matrix])
        for item in sparse_matrix:
            item[column_index] -= min_unit

    return sparse_matrix
