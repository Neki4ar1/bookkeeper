# -*- coding: utf8 -*-
"""
Демонстрация TableView
на основе https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/
"""
import sys

from PySide6.QtWidgets import QApplication
from bookkeeper.view.expense_view import MainWindow
from bookkeeper.view.redactor_view import RedactorWindow
from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQliteRepository


DB_NAME = 'test.db'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    VIEW = MainWindow()
    MODEL = None  # TODO: здесь должна быть модель
    cat_repo = SQliteRepository[Category](DB_NAME, Category)
    exp_repo = SQliteRepository[Expense](DB_NAME, Expense)
    bud_repo = SQliteRepository[Budget](DB_NAME, Budget)

    window = ExpensePresenter(MODEL, VIEW, [cat_repo, exp_repo, bud_repo])
    window.show()
    app.exec()
