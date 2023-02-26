import sqlite3 as sq
from inspect import get_annotations
from typing import Any
from dataclasses import dataclass

from bookkeeper.repository.abstract_repository import AbstractRepository, T


def make_t_obj(cls, fields: dict, values: str):
    res = object.__new__(cls)  # Создаём объект класса, который будем возвращать
    if values is None:
        return None
    for attr, val in zip(fields.keys(), values):  # Заполняем его данными из полученной строки из БД
        # print(attr, val)
        setattr(res, attr, val)
    setattr(res, 'pk', values[-1])
    return res


class SQliteRepository(AbstractRepository[T]):

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)   # Словарь аннотаций из класса, который передан
        self.fields.pop('pk')
        self.cls = cls

        with sq.connect(self.db_file) as con:
            cur = con.cursor()
            placeholders = ' '.join([f"{field} TEXT," for field in self.fields])
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({placeholders} pk INTEGER PRIMARY KEY)")
        con.close()

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
            for attr, val in zip(self.fields.keys(), values):     # Заполняем его данными из полученной строки из БД
                setattr(res, attr, val)
            res.pk = pk
        con.close()
        return res

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sq.connect(self.db_file) as con:
            cur = con.cursor()
            if where is None:
                cur.execute(f"SELECT * FROM {self.table_name}")
            else:
                placeholders = ', '.join(x + "=?" for x in where.keys())
                values = [getattr(where, x) for x in where]
                cur.execute(f"SELECT * FROM {self.table_name} WHERE {placeholders}", values)
            values = cur.fetchall()
            res = [make_t_obj(self.cls, self.fields, val) for val in values]
        con.close()
        return res

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        placeholders = ', '.join(x+"=?" for x in obj.fields.keys())
        values = [getattr(obj, x) for x in self.fields]
        with sq.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"UPDATE {self.table_name} SET {placeholders} WHERE rowid = {obj.pk})", values)
            obj.pk = cur.lastrowid
        con.close()

    def delete(self, pk: int) -> None:
        with sq.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM {self.table_name} WHERE rowid = {pk}")
        con.close()
#
# r = SQliteRepository('test.sqlite', Test)
# o = Test('John')
# r.add(o)