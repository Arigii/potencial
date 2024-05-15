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
