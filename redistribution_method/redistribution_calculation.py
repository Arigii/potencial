from redistribution_method.create_zero_list import create_zero_vector
from redistribution_method.vectors_multiplication import vectors_multiplication


def redistribution_calculation(cost_matrix: list[list[int]], storages: list[int], shops: list[int], item_cors: list[int]):
    item_value = cost_matrix[item_cors[0]][item_cors[1]]
    supply_vector = create_zero_vector(len(storages), item_cors[0], item_value)
    shop_vector = create_zero_vector(len(shops), item_cors[1], item_value)
    delta = vectors_multiplication(shop_vector, shops) - vectors_multiplication(supply_vector, storages)
    return delta
