from bookkeeper.models.expense import Expense


class ExpensePresenter:

    def __init__(self, model, view, cat_repo, exp_repo):
        self.model = model
        self.view = view
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        self.exp_data = [[tup.added_date, tup.amount, tup.category, tup.comment] for tup in self.exp_repo.get_all()]
        self.cat_data = [[cat.name, cat.parent, cat.pk] for cat in cat_repo.get_all()]
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)

    def update_expense_data(self):
        self.exp_data = [[tup.added_date, tup.amount, tup.category, tup.comment] for tup in self.exp_repo.get_all()]
        self.view.set_expense_table(self.exp_data)

    def show(self):
        self.view.show()
        self.update_expense_data()
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self):
        amount, category, comment = self.view.get_am_cat_com()
        # category = self.view.get_selected_cat()
        # amount = self.view.get_amount()
        exp = Expense(amount=float(amount), category=category, comment=comment)
        self.exp_repo.add(exp)
        self.update_expense_data()
