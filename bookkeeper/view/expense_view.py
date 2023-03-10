# -*- coding: utf8 -*-
"""
Главный файл, отвечающий за внешний вид
"""
from typing import Any

from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QWidget,
    QGridLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
    QMainWindow
)
from PySide6 import QtCore, QtWidgets
from bookkeeper.repository.abstract_repository import T
from bookkeeper.view.redactor_view import RedactorWindow


class TableModel(QtCore.QAbstractTableModel):
    """
    class that making tables to view
    data
    rowCount
    columnCount
    headerData
    """
    def __init__(self, data: list[Any], columns: list[str]):
        super(TableModel, self).__init__()
        self._data = data
        self.columns = columns

    def data(self, index: Any, role: Any) -> Any | None:
        """
        See below for the nested-list data structure.
        .row() indexes into the outer list,
        .column() indexes into the sub-list
        """
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def rowCount(self, index: Any) -> Any:
        """The length of the outer list."""
        return len(self._data)

    def columnCount(self, index: Any) -> Any:
        """
        The following takes the first sub-list, and returns
        the length (only works if all rows are an equal length)
        """
        return len(self._data[0])

    def headerData(self, section: Any, orientation: Any, role: Any) -> str | None:
        """section is the index of the column/row."""
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self.columns[section])
        return None


class MainWindow(QMainWindow):
    """
    MainWindow class of editing Main Window
    Methods:
        set_expense_table
        set_budget_tabel
        set_category_dropdown
        on_expense_add_button_clicked
        get_amount
        get_selected_cat
        get_comment
        get_am_cat_com
    """
    def __init__(self) -> None:
        super().__init__()
        self.redactor_w = RedactorWindow()

        self.setWindowTitle("Программа для ведения бюджета")
        self.setFixedSize(500, 700)

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel('Последние расходы'))

        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)

        self.layout.addWidget(QLabel('Бюджет'))
        self.budget_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.budget_grid)

        self.bottom_controls = QGridLayout()
        self.bottom_controls.addWidget(QLabel('Сумма'), 0, 0)

        self.amount_line_edit = QLineEdit()

        self.bottom_controls.addWidget(self.amount_line_edit, 0, 1)
        self.bottom_controls.addWidget(QLabel('Категория'), 1, 0)

        self.category_dropdown = QComboBox()

        self.bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.edit_button = QPushButton('Редактировать')
        self.bottom_controls.addWidget(self.edit_button, 1, 2)

        self.bottom_controls.addWidget(QLabel('Комментарий'), 2, 0)

        self.commentary_line_edit = QLineEdit()
        self.bottom_controls.addWidget(self.commentary_line_edit, 2, 1)

        self.expense_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 3, 1)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def set_expense_table(self, data: list[T]) -> None:
        """making expense table on main window"""
        cat_model = TableModel(data[::-1], ['Дата', 'Сумма', 'Категория', 'Комментарий'])
        self.expenses_grid.setModel(cat_model)
        self.expenses_grid.horizontalHeader().setStretchLastSection(True)

    def set_budget_table(self, data: list[T]) -> None:
        """making budget table on main window"""
        bud_model = TableModel(data, ['', 'Бюджет', 'Потрачено'])
        self.budget_grid.setModel(bud_model)
        self.budget_grid.horizontalHeader().setStretchLastSection(True)
        self.budget_grid.verticalHeader().setStretchLastSection(True)

    def set_category_dropdown(self, data: list[str]) -> None:
        """make dropdown of categories on main window"""
        self.category_dropdown.clear()
        self.category_dropdown.addItems([tup[0] for tup in data])

    def on_expense_add_button_clicked(self, slot: Any) -> None:
        """connect to funtion slot after clicking button"""
        self.expense_add_button.clicked.connect(slot)

    def on_redactor_add_button_clicked(self, slot: Any) -> None:
        self.edit_button.clicked.connect(slot)

    def get_redactor(self):
        return self.redactor_w

    def get_amount(self) -> float:
        """return amount"""
        return float(self.amount_line_edit.text())  # TODO: обработка исключений

    def get_selected_cat(self) -> Any:
        """return category"""
        return self.category_dropdown.currentText()

    def get_comment(self) -> Any:
        """return comment"""
        return self.commentary_line_edit.text()

    def get_am_cat_com(self) -> list[Any]:
        """return list[amount, category, comment]"""
        return [self.get_amount(), self.get_selected_cat(), self.get_comment()]
