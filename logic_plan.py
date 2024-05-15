def oporn_plan(cost_matrix: list[list[int]], storages: list[int], shops: list[int]):
    num_storages = len(storages)
    num_shops = len(shops)

    # Создаем копию матрицы стоимостей для работы
    matrix = [row[:] for row in cost_matrix]

    # Инициализируем пустой опорный план
    plan = [[0] * num_shops for _ in range(num_storages)]

    # Пока есть неудовлетворенные потребности магазинов
    while sum(shops) > 0:
        # Находим минимальное значение в матрице стоимостей
        min_cost = float('inf')
        min_i, min_j = -1, -1
        for i in range(num_storages):
            for j in range(num_shops):
                if matrix[i][j] < min_cost:
                    min_cost = matrix[i][j]
                    min_i, min_j = i, j

        # Выполняем перевозку ресурса с минимальной стоимостью
        if storages[min_i] >= shops[min_j]:
            plan[min_i][min_j] = shops[min_j]
            storages[min_i] -= shops[min_j]
            shops[min_j] = 0
            # Удаляем столбец, так как потребность магазина удовлетворена
            for i in range(num_storages):
                matrix[i][min_j] = float('inf')
        else:
            plan[min_i][min_j] = storages[min_i]
            shops[min_j] -= storages[min_i]
            storages[min_i] = 0
            # Удаляем строку, так как ресурс производителя исчерпан
            for j in range(num_shops):
                matrix[min_i][j] = float('inf')

    return plan


def calculate_potentials(cost_matrix, initial_plan):
    num_rows = len(cost_matrix)
    num_cols = len(cost_matrix[0])

    # Initialize potentials
    u = [None] * num_rows
    v = [None] * num_cols
    u[0] = 0  # Arbitrarily set the first potential to 0

    # Loop until all potentials are determined
    iterations = 0
    while (None in u or None in v) and iterations < 1000:
        for i in range(num_rows):
            for j in range(num_cols):
                if initial_plan[i][j] != 0:
                    if u[i] is not None and v[j] is None:
                        v[j] = cost_matrix[i][j] - u[i]
                    elif u[i] is None and v[j] is not None:
                        u[i] = cost_matrix[i][j] - v[j]
        iterations += 1

    return is_optimal(cost_matrix, initial_plan, u, v)


def is_optimal(cost_matrix, initial_plan, u, v):
    num_rows = len(cost_matrix)
    num_cols = len(cost_matrix[0])
    for i in range(num_rows):
        for j in range(num_cols):
            if initial_plan[i][j] == 0:
                if cost_matrix[i][j] - u[i] - v[j] < 0:
                    return False
    return True


def redistribute(cost_matrix, initial_plan, u, v):
    num_rows = len(cost_matrix)
    num_cols = len(cost_matrix[0])

    # Initialize closed list
    closed = [[False] * num_cols for _ in range(num_rows)]

    # Find cells to be closed
    for i in range(num_rows):
        for j in range(num_cols):
            if initial_plan[i][j] > 0:
                if not closed[i][j] and cost_matrix[i][j] - u[i] - v[j] != 0:
                    closed[i][j] = True

    # Continue until no more cells can be closed
    while True:
        # Find an unclosed cell
        unclosed_cell = None
        for i in range(num_rows):
            for j in range(num_cols):
                if not closed[i][j]:
                    unclosed_cell = (i, j)
                    break
            if unclosed_cell:
                break

        if not unclosed_cell:
            break  # No more unclosed cells

        # Initialize the path with the unclosed cell
        path = [unclosed_cell]
        closed[unclosed_cell[0]][unclosed_cell[1]] = True

        # Try to find a closed cell adjacent to the last cell in the path
        while True:
            current_cell = path[-1]
            found_adjacent_closed = False

            # Check adjacent cells
            for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                next_cell = (current_cell[0] + di, current_cell[1] + dj)

                # Check if the next cell is within bounds
                if 0 <= next_cell[0] < num_rows and 0 <= next_cell[1] < num_cols:
                    if closed[next_cell[0]][next_cell[1]]:
                        found_adjacent_closed = True
                        break

            if not found_adjacent_closed:
                break  # No more adjacent closed cells

            # Find the closed cell with the smallest marginal cost
            min_marginal_cost = float('inf')
            min_marginal_cost_cell = None
            for i in range(num_rows):
                for j in range(num_cols):
                    if closed[i][j]:
                        marginal_cost = cost_matrix[i][j] - u[i] - v[j]
                        if marginal_cost < min_marginal_cost:
                            min_marginal_cost = marginal_cost
                            min_marginal_cost_cell = (i, j)

            # Add the cell to the path and mark it as closed
            path.append(min_marginal_cost_cell)
            closed[min_marginal_cost_cell[0]][min_marginal_cost_cell[1]] = False

        # Update the plan along the path
        min_quantity = min(initial_plan[cell[0]][cell[1]] for cell in path)
        for cell in path:
            initial_plan[cell[0]][cell[1]] -= min_quantity

        # Find the cell with the smallest quantity along the path
        min_quantity_cell = min(path, key=lambda cell: initial_plan[cell[0]][cell[1]])

        # Adjust the plan to satisfy the closed cells
        initial_plan[min_quantity_cell[0]][min_quantity_cell[1]] += min_quantity

    return initial_plan
