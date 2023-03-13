from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide6.QtWidgets import QApplication
from bookkeeper.view.expense_view import MainWindow

import pytest

@pytest.fixture(scope="module")
def app(qtbot):
    """
    Pytest fixture for the application
    """
    app = QApplication([])
    qtbot.addWidget(MainWindow())
    return app

def test_add_expense(app):
    """
    Testing expense adding
    """
    main_window = app.topLevelWidgets()[0]
    expense_add_button = main_window.expense_add_button
    amount_line_edit = main_window.amount_line_edit
    commentary_line_edit = main_window.commentary_line_edit
    category_dropdown = main_window.category_dropdown

    # Set up the combo box for selecting categories
    category_dropdown.clear()
    category_dropdown.setModel(QStandardItemModel())
    categories_model = category_dropdown.model()
    for category_name in ['food', 'transport', 'housing', 'entertainment']:
        categories_model.appendRow(QStandardItem(category_name))

    # Set up the line edit fields
    amount_line_edit.setPlainText('200')
    commentary_line_edit.setPlainText('test comment')
    category_dropdown.setCurrentIndex(3)

    # Add the expense
    qtbot.mouseClick(expense_add_button, Qt.LeftButton)

    # Check if the expense is added
    expense_table = main_window.expenses_grid
    assert expense_table.model().rowCount() == 1
    expense_amount = expense_table.model().data(expense_table.model().index(0, 0))
    assert expense_amount == '200.0'
    expense_category = expense_table.model().data(expense_table.model().index(0, 1))
    assert expense_category == 'entertainment'
    expense_comment = expense_table.model().data(expense_table.model().index(0, 2))
    assert expense_comment == 'test comment'
