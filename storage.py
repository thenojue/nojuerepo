from datetime import date
from typing import List

import model


class StorageException(Exception):
    pass


class LocalStorage:
    def __init__(self):
        self._id_counter = 0
        self._storage = {}

    def create(self, event: model.Event) -> str:
        self._id_counter += 1
        event.id = self._id_counter
        self._storage[event.date] = event
        return str(event.id)

    def get_all(self) -> list[model.Event]:
        return list(self._storage.values())

    def get(self, _id: date) -> model.Event:
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        return self._storage[_id]

    def update(self, _id: str, event: model.Event):
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        event.date = _id
        self._storage[event.date] = event

    def delete(self, _id: str):
        if _id not in self._storage:
            raise StorageException(f"{_id} not found in storage")
        del self._storage[_id]
