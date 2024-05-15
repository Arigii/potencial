def copy_int_vector(vector: list[int]) -> list[int]:
    return [item for item in vector]


def copy_int_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return [row[:] for row in matrix]
