def vectors_multiplication(first_vector: list[int], second_vector: list[int]) -> int:
    return sum(x * y for x, y in zip(first_vector, second_vector))
