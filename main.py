import random
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox, QSpinBox, \
    QSizePolicy, QLabel
from PyQt5.uic import loadUi

from logic_plan import first_plan


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("untitled.ui", self)

        # Устанавливаем количество строк и столбцов для таблицы
        self.tableWidget.setRowCount(self.spinBox_rows.value())
        self.tableWidget.setColumnCount(self.spinBox_columns.value())

        # Подключаем сигналы от spinBox'ов к слотам для обновления таблицы
        self.spinBox_rows.valueChanged.connect(self.update_table_rows)
        self.spinBox_columns.valueChanged.connect(self.update_table_columns)

        # Создаем модель данных для tableWidget_2
        self.tableWidget_2.setRowCount(self.tableWidget.rowCount())
        self.tableWidget_2.setColumnCount(self.tableWidget.columnCount())

        self.pushButton.clicked.connect(self.copy_table_values)

        QTimer.singleShot(100, self.fill_table_with_indices)

    def fill_table_with_indices(self):
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)

        self.tableWidget.setColumnCount(self.spinBox_columns.value() + 1)
        self.tableWidget.setRowCount(self.spinBox_rows.value() + 1)

        self.tableWidget_2.setColumnCount(self.spinBox_columns.value() + 1)
        self.tableWidget_2.setRowCount(self.spinBox_rows.value() + 1)

        rows = self.tableWidget.rowCount()
        columns = self.tableWidget.columnCount()

        storages_headers = []
        for supplier in range(1, self.spinBox_columns.value() + 1):
            storages_headers.append(f'Магазин {str(supplier)}')

        shop_headers = []
        for supplier in range(1, self.spinBox_rows.value() + 1):
            shop_headers.append(f'Поставщик {str(supplier)}')

        for row in range(rows):
            for column in range(columns):
                label = QLabel(self)
                if type(self.tableWidget.cellWidget(row, column)) != QSpinBox(self) and not (
                        row == self.tableWidget.rowCount() - 1 and column == self.tableWidget.columnCount() - 1
                ):
                    spin_box = QSpinBox(self)
                    spin_box.setValue(random.randint(1, 30))
                    self.tableWidget.setCellWidget(row, column, spin_box)
                elif row == self.tableWidget.rowCount() - 1 and column == self.tableWidget.columnCount() - 1:
                    self.tableWidget.setCellWidget(row, column, label)

        self.tableWidget.setHorizontalHeaderLabels(storages_headers + ['Запасы'])
        self.tableWidget.setVerticalHeaderLabels(shop_headers + ['Потребности'])

        label = QLabel(self)
        self.tableWidget_2.setCellWidget(self.tableWidget.rowCount(), 0, label)

        self.tableWidget_2.setHorizontalHeaderLabels(storages_headers + ['Запасы'])
        self.tableWidget_2.setVerticalHeaderLabels(shop_headers + ['Потребности'])

        self.resize_cell_table()

    def resizeEvent(self, a0, QResizeEvent=None):
        self.resize_cell_table()

    def resize_cell_table(self):
        width = max(150, (self.tableWidget.width() - 150) // (self.spinBox_columns.value() + 1))
        height = max(50, (self.tableWidget.height() - 30) // (self.spinBox_rows.value() + 1))

        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHeight(row, height)
            self.tableWidget_2.setRowHeight(row, height)

        height = max(60, (self.tableWidget.height()) // (self.spinBox_rows.value() + 1))
        self.tableWidget_2.setRowHeight(self.tableWidget.rowCount(), height)
        self.tableWidget_2.setSpan(self.tableWidget.rowCount(), 0, self.tableWidget.rowCount(),
                                   self.tableWidget.columnCount())

        for column in range(self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(column, width)
            self.tableWidget_2.setColumnWidth(column, width)

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
