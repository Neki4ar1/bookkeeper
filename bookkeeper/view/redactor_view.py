import sys
from random import randint

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
        category_line = QLineEdit()
        bottom_controls.addWidget(category_line, 0, 1)

        edit_button = QPushButton('save')
        # edit_button.clicked.connect(self.show_redactor())
        bottom_controls.addWidget(edit_button, 0, 2)

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
