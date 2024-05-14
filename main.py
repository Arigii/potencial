import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.uic import loadUi

from logic_plan import first_plan


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("untitled.ui", self)

        # Устанавливаем количество строк и столбцов для таблицы
        self.tableWidget.setRowCount(self.spinBox_rows.value())
        self.tableWidget.setColumnCount(self.spinBox_columns.value())

        self.fill_table_with_indices()

        # Подключаем сигналы от spinBox'ов к слотам для обновления таблицы
        self.spinBox_rows.valueChanged.connect(self.update_table_rows)
        self.spinBox_columns.valueChanged.connect(self.update_table_columns)

        # Создаем модель данных для tableWidget_2
        self.tableWidget_2.setRowCount(self.tableWidget.rowCount())
        self.tableWidget_2.setColumnCount(self.tableWidget.columnCount())

        self.pushButton.clicked.connect(self.copy_table_values)

        # Устанавливаем режим растягивания столбцов
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def fill_table_with_indices(self):
        rows = self.tableWidget.rowCount()
        columns = self.tableWidget.columnCount()
        for row in range(rows):
            for column in range(columns):
                if row == 0 and column == 0:
                    pass
                elif row == 0:
                    index = f"Потребитель {column}"
                    self.tableWidget.setItem(row, column, QTableWidgetItem(index))
                elif column == 0:
                    index = f"Поставщик {row}"
                    self.tableWidget.setItem(row, column, QTableWidgetItem(index))
                elif column != columns - 1 and row != rows - 1:
                    index = f"Тариф i{row + 1}j{column + 1}"
                    self.tableWidget.setItem(row, column, QTableWidgetItem(index))
                else:
                    index = "Потребность"
                    self.tableWidget.setItem(row, column, QTableWidgetItem(index))
        supplier_volume_item = QTableWidgetItem("Объем поставщика")
        customer_volume_item = QTableWidgetItem("Запасы")
        space_cell = QTableWidgetItem("")
        self.tableWidget.setItem(rows - 1, 0, supplier_volume_item)
        self.tableWidget.setItem(0, columns - 1, customer_volume_item)
        self.tableWidget.setItem(rows - 1, columns - 1, space_cell)

    def update_table_rows(self, value):
        self.tableWidget.setRowCount(value)
        self.fill_table_with_indices()
        self.tableWidget_2.setRowCount(value)

    def update_table_columns(self, value):
        self.tableWidget.setColumnCount(value)
        self.fill_table_with_indices()
        self.tableWidget_2.setColumnCount(value)

    def copy_table_values(self):
        rows = self.tableWidget.rowCount()
        columns = self.tableWidget.columnCount()
        data = []
        sum_columns = 0
        sum_rows = 0
        for row in range(1, rows):
            row_data = []
            for column in range(1, columns):
                item = self.tableWidget.item(row, column)
                if item is not None:
                    text = item.text()
                    if text.isdigit() or (text.startswith('-') and text[1:].isdigit()):
                        row_data.append(int(text))
                        if column == columns - 1 and row != 0 and row != rows - 1:
                            sum_columns += int(text)
                        elif row == rows - 1 and column != 0 and column != columns - 1:
                            sum_rows += int(text)
                    elif column == columns - 1 and row == rows - 1:
                        pass
                    else:
                        QMessageBox.critical(self, "Ошибка", f"Невозможно собрать значение '{text}' из таблицы, "
                                                             f"так как оно не является числом. {row} {column}")
                        return
            data.append(row_data)

        if sum_rows != sum_columns:
            QMessageBox.critical(self, "Ошибка", "Невозможно построить план с задачей открытого типа")
            return

        data = first_plan(data)
        print(data)
        return

        # Выводим данные в консоль (здесь можно провести другие операции с данными)
        print("Собранные данные:", data)
        rows = self.tableWidget.rowCount()
        columns = self.tableWidget.columnCount()
        for row in range(rows):
            for column in range(columns):
                if row == 0 or column == 0:
                    item = self.tableWidget.item(row, column)
                    if item is not None:
                        text = item.text()
                        self.tableWidget_2.setItem(row, column, QTableWidgetItem(text))
                """else:
                    item = data[row][column]
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(item))"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
