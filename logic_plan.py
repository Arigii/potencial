def first_plan(data):
    # Получаем размеры таблицы из данных
    rows = len(data)
    columns = len(data[0])

    # Создаем пустой опорный план
    initial_plan = [[0] * columns for _ in range(rows)]

    # Проходим по строкам и столбцам таблицы
    for i in range(rows):
        for j in range(columns):
            # Проверяем, существует ли значение по данному индексу
            if i < rows - 1 and j < columns - 1:  # исключаем последнюю строку и последний столбец
                # Если ячейка не пуста, то копируем значение в опорный план
                if data[i][j]:
                    initial_plan[i][j] = data[i][j]

    return initial_plan


def min_from_table():
    pass
