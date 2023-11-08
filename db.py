from datetime import date
from typing import List

import model
import storage


class DBException(Exception):
    pass


class EventDB:
    def __init__(self):
        self._storage = storage.LocalStorage()

    def create(self, event: model.Event) -> str:
        try:
            return self._storage.create(event)
        except Exception as ex:
            raise DBException(f"failed CREATE operation with: {ex}")

    def get_all(self) -> List[model.Event]:
        try:
            return self._storage.get_all()
        except Exception as ex:
            raise DBException(f"failed LIST operation with: {ex}")

    def get(self, date: date) -> model.Event:
        try:
            return self._storage.get(date)
        except Exception as ex:
            raise DBException(f"failed READ operation with: {ex}")

    def update(self, _id: str, note: model.Event):
        try:
            return self._storage.update(_id, note)
        except Exception as ex:
            raise DBException(f"failed UPDATE operation with: {ex}")

    def delete(self, _id: str):
        try:
            return self._storage.delete(_id)
        except Exception as ex:
            raise DBException(f"failed DELETE operation with: {ex}")
