# -*- coding: utf8 -*-
"""
module of redactor window
"""

from typing import Any

from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QLabel,
    QWidget,
    QGridLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
)


class RedactorWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Redactor')
        layout = QVBoxLayout()

        bottom_controls = QGridLayout()

        bottom_controls.addWidget(QLabel("add category"), 0, 0)
        self.category_line = QLineEdit()
        bottom_controls.addWidget(self.category_line, 0, 1)

        self.save_button = QPushButton('save')
        # edit_button.clicked.connect(self.show_redactor())
        bottom_controls.addWidget(self.save_button, 0, 2)

        bottom_controls.addWidget(QLabel("delete category"), 1, 0)
        category_delete = QLineEdit()
        bottom_controls.addWidget(category_delete, 1, 1)

        delete_button = QPushButton('delete')
        # edit_button.clicked.connect(self.show_redactor())
        bottom_controls.addWidget(delete_button, 1, 2)

        bottom_controls.addWidget(QLabel("Set Budget"), 2, 0)

        budget_dropdown = QComboBox()
        budget_dropdown.addItems(['day', 'week', 'month'])
        bottom_controls.addWidget(budget_dropdown, 3, 1)
        set_budget = QLineEdit()
        bottom_controls.addWidget(set_budget, 2, 1)

        set_budget_button = QPushButton('set')
        bottom_controls.addWidget(set_budget_button, 2, 2)

        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_controls)

        layout.addWidget(bottom_widget)

        # self.widget = QWidget()
        self.setLayout(layout)

    def on_add_category_clicked(self, slot):
        self.save_button.clicked.connect(slot)

    def get_add_category(self) -> str:
        """return amount"""
        return self.category_line.text()

    # def get_selected_cat(self) -> Any:
    #     """return category"""
    #     return self.category_dropdown.currentText()
    #
    # def get_comment(self) -> Any:
    #     """return comment"""
    #     return self.commentary_line_edit.text()
    #
    # def get_am_cat_com(self) -> list[Any]:
    #     """return list[amount, category, comment]"""
    #     return [self.get_amount(), self.get_selected_cat(), self.get_comment()]
