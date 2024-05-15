import random
import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSpinBox, QLabel, QLCDNumber
from PyQt5.uic import loadUi

from logic_plan import oporn_plan, calculate_potentials
from redistribution_method.redistribution_method import redistribution_method


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.storages = None
        self.cost_matrix = None
        self.shops = None
        loadUi("untitled.ui", self)

        # Устанавливаем количество строк и столбцов для таблицы
        self.tableWidget.setRowCount(self.spinBox_rows.value())
        self.tableWidget.setColumnCount(self.spinBox_columns.value())

        # Подключаем сигналы от spinBox'ов к слотам для обновления таблицы
        self.spinBox_rows.valueChanged.connect(self.fill_table_with_indices)
        self.spinBox_columns.valueChanged.connect(self.fill_table_with_indices)

        # Создаем модель данных для tableWidget_2
        self.tableWidget_2.setRowCount(self.tableWidget.rowCount())
        self.tableWidget_2.setColumnCount(self.tableWidget.columnCount())

        self.pushButton.clicked.connect(self.extract_data)

        QTimer.singleShot(100, self.fill_table_with_indices)

    def extract_cost_matrix(self):
        cost_matrix = []
        for row in range(self.spinBox_rows.value()):
            row_data = []
            for column in range(self.spinBox_columns.value()):
                spin_box = self.tableWidget.cellWidget(row, column)
                row_data.append(spin_box.value())
            cost_matrix.append(row_data)
        return cost_matrix

    def extract_storages(self):
        storages = []
        for row in range(self.spinBox_rows.value()):
            spin_box = self.tableWidget.cellWidget(row, self.spinBox_columns.value())
            if type(spin_box) is QSpinBox:
                storages.append(spin_box.value())
                label = QLabel()
                label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                label.setText(str(spin_box.value()))
                self.tableWidget_2.setCellWidget(row, self.spinBox_columns.value(), label)
        return storages

    def extract_shops(self):
        shops = []
        for column in range(self.spinBox_columns.value()):
            spin_box = self.tableWidget.cellWidget(self.spinBox_rows.value(), column)
            if type(spin_box) is QSpinBox:
                shops.append(spin_box.value())
                label = QLabel()
                label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                label.setText(str(spin_box.value()))
                self.tableWidget_2.setCellWidget(self.spinBox_rows.value(), column, label)
        return shops

    def extract_data(self):
        self.cost_matrix = self.extract_cost_matrix()
        self.storages = self.extract_storages()
        self.shops = self.extract_shops()
        if sum(self.storages) != sum(self.shops):
            QMessageBox.critical(self, "Ошибка",
                                 "Невозможно построить план у задачи открытого типа")
            return
        try:
            result, result_summ = redistribution_method(self.cost_matrix, self.storages, self.shops)
            # success = calculate_potentials(self.cost_matrix, result)
            # if not success:
            #     QMessageBox.critical(self, "Внимание", "Опорный план будет оптимизирован потенциальным методом")

            for row_index in range(len(result)):
                for column_index in range(len(result[row_index])):
                    label = QLabel()
                    value = result[row_index][column_index]
                    label.setText(str(value) if value != 0 else '')
                    label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                    self.tableWidget_2.setCellWidget(row_index, column_index, label)
            self.lcdNumber.display(result_summ)
        except RecursionError:
            QMessageBox.critical(self, "Внимание", "Оптимальное решение для данной задачи найти не возможно")

    def fill_table_with_indices(self):
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
