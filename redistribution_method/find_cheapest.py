from redistribution_method.constants import IMPOSSIBLE_CORS, IMPOSSIBLE_VALUE
from redistribution_method.replace_items_by_index import replace_item_by_index


def find_cheapest(matrix: list[list[int]], ignoring_rows: list[int] = (),
                  ignoring_columns: list[int] = ()) -> list[int]:
    cheapest = IMPOSSIBLE_CORS

    for row_index in range(len(matrix)):
        checking_row = replace_item_by_index(matrix[row_index], ignoring_rows, IMPOSSIBLE_VALUE)
        for item_index in range(len(checking_row)):
            if checking_row[item_index] < matrix[cheapest[0]][cheapest[1]] and item_index not in ignoring_columns:
                cheapest = [row_index, item_index]

    return cheapest
