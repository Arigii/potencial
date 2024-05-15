def create_zero_vector(len_vector: int, item_position: int, item_value: int) -> list[int]:
    vector = [0 for _ in range(len_vector)]
    vector[item_position] = item_value
    return vector


def create_zero_matrix(rows: int, columns: int) -> list[list[int]]:
    return [[0 for _ in range(rows)] for _ in range(columns)]
