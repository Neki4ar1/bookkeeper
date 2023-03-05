# -*- coding: utf8 -*-
"""
Демонстрация TableView на основе https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/
"""

from PySide6.QtWidgets import QApplication
from bookkeeper.view.expense_view import MainWindow
from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQliteRepository

import sys

DB_NAME = 'test.db'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainWindow()
    model = None  # TODO: здесь должна быть модель
    cat_repo = SQliteRepository[Category](DB_NAME, Category)
    exp_repo = SQliteRepository[Expense](DB_NAME, Expense)

    window = ExpensePresenter(model, view, cat_repo, exp_repo)  # TODO: передать три репозитория
    window.show()
    app.exec()
