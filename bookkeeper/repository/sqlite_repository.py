import sqlite3 as sq
from inspect import get_annotations

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQliteRepository(AbstractRepository[T]):

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)   # Словарь аннотаций из класса, который передан
        self.fields.pop('pk')
        self.cls = cls

    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        placeholders = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sq.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f"INSERT INTO {self.table_name} ({names}) VALUES({placeholders})", values)
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        with sq.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {self.table_name} WHERE rowid = {pk}")
            res = self.cls()    # Создаём объект класса, который будем возвращать
            if (values := cur.fetchone()) is None:
                return None
            else:
                for attr, val in zip(self.fields, values):     # Заполняем его данными из полученной строки из БД
                    setattr(res, attr, val)
                res.pk = pk
        con.close()
        return res

    def get_all(self):
        ...

    def update(self):
        ...

    def delete(self):
        ...