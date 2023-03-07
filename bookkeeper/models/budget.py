# -*- coding: utf8 -*-
"""
Описан класс, представляющий бюджет на день/неделю/месяц
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Budget:
    """
    Бюджет
    limit - limit on period
    spent - how much money have been spent in period
    period - day, week, or month
    pk - primary key
    """
    limit: float
    spent: float
    period: str
    pk: int = 0

    def __init__(self, limit, spent, period, pk):
        self.limit = limit
        self.spent = spent
        self.period = period
        self.pk = pk

    def set_limit_bud(self, limit: float) -> None:
        self.limit = limit

