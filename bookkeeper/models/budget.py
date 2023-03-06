"""
ќписан класс, представл€ющий бюджет на день/неделю/мес€ц
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Budget:
    """
    Ѕюджет

    """
    r_day: float = 0
    r_week: float = 0*7
    r_month: float = 0*30
    pk: int = 0
