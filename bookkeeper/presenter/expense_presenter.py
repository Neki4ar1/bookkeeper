# -*- coding: utf8 -*-
"""
module that connetn view and repository
"""
import datetime
from typing import Any

from bookkeeper.models.expense import Expense


class ExpensePresenter:
    """
    class that present and update expenses and budget

    Methods:
        update_expense_data - method that update expense in table
        update_budget_data - method that update budget in table
        show - start point of main window
        handle_expense_add_button_clicked - add expense when button clicked
    """

    def __init__(self, model: Any, view: Any, repo: list[Any]):
        self.model = model
        self.view = view
        self.repos = repo
        # self.cat_repo = repo[0]
        # self.exp_repo = repo[1]
        # self.bud_repo = repo[2]
        self.bud_data = [[bud.limit_on, bud.spent] for bud in self.repos[2].get_all()]
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)
        self.view.on_redactor_add_button_clicked(self.show_redactor)

    def update_expense_data(self) -> None:
        """update information"""
        exp_data = [[tup.added_date,
                     tup.amount,
                     tup.category,
                     tup.comment]
                    for tup in self.repos[1].get_all()]
        # d_m_y = int(str(self.exp_data[-1][0])[:10])
        # for date, amount, cat, com in self.exp_data:
        #     day_sum = day_sum + (amount if d_m_y == int(str(date)[:10]) else 0)
        #     made = by_neki4ar
        #     week_sum =
        self.update_budget_data()
        self.view.set_expense_table(exp_data)

    def update_budget_data(self) -> None:
        """updates budget"""
        today = f"{datetime.datetime.utcnow():%d-%m-%Y %H:%M}"
        week_day = datetime.datetime.utcnow().weekday()

        week_dates = [f"{datetime.datetime.utcnow()-datetime.timedelta(i):%d-%m-%Y %H:%M}"
                      for i in range(week_day)]
        week_data: list[Any] = []
        for date in week_dates:
            week_data = week_data+self.repos[1].get_like({"added_date": f"{date[:10]}%"})
        # print(*week_data, sep='\n')

        today_data = [float(day.amount)
                      for day in self.repos[1].get_like({"added_date": f"{today[:10]}%"})]
        week_data = [float(day.amount) for day in week_data]
        month_data = [float(m.amount)
                      for m in self.repos[1].get_like({"added_date": f"%{today[2:10]}%"})]

        data = [
            ['День', f'{self.bud_data[0][0]}', sum(today_data)],
            ['Неделя', f'{self.bud_data[1][0]}', sum(week_data)],
            ['Месяц', f'{self.bud_data[2][0]}', sum(month_data)],
        ]
        self.view.set_budget_table(data)

    def show_redactor(self, checked):
        red_w = self.view.get_redactor()
        if red_w.isVisible():
            red_w.hide()
        else:
            red_w.show()

    def show(self) -> None:
        """showing all on main view"""
        self.view.show()
        self.update_expense_data()
        self.update_budget_data()
        cat_data = [[cat.name, cat.parent, cat.pk] for cat in self.repos[0].get_all()]
        self.view.set_category_dropdown(cat_data)

    def handle_expense_add_button_clicked(self) -> None:
        """add expense and update expense on expense_table"""
        amount, category, comment = self.view.get_am_cat_com()
        exp = Expense(amount=float(amount), category=category, comment=comment)
        self.repos[1].add(exp)
        self.update_expense_data()
