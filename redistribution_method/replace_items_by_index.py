from redistribution_method.constants import NEGATIVE_IMPOSSIBLE_VALUE


def replace_item_by_index(vector: list[int], indexes_of_deleted_items: list[int],
                          new_value: int = NEGATIVE_IMPOSSIBLE_VALUE) -> list[int]:
    for index in indexes_of_deleted_items:
        vector[index] = new_value
    return vector
