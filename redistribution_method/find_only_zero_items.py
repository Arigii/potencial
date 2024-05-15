from redistribution_method.replace_items_by_index import replace_item_by_index


def find_only_zero_items(
        sparse_matrix: list[list[int]],
        cost_matrix: list[list[int]],
        ignoring_rows: list[int] = (),
        ignoring_columns: list[int] = ()
) -> list[int]:
    zero_items_cors = []

    for row_index in range(len(sparse_matrix)):
        checking_row = replace_item_by_index(sparse_matrix[row_index], ignoring_columns)
        if checking_row.count(0) == 1 and row_index not in ignoring_rows:
            zero_items_cors.append([row_index, sparse_matrix[row_index].index(0)])

    for column_index in range(len(sparse_matrix[0])):
        column = replace_item_by_index([item[column_index] for item in sparse_matrix], ignoring_rows)
        if column.count(0) == 1 and column_index not in ignoring_columns:
            zero_items_cors.append([column.index(0), column_index])

    if not zero_items_cors:
        return []

    response_zero_item = zero_items_cors[0]

    for zero_item in zero_items_cors:
        if cost_matrix[zero_item[0]][zero_item[1]] < cost_matrix[response_zero_item[0]][response_zero_item[1]]:
            response_zero_item = zero_item

    return response_zero_item
