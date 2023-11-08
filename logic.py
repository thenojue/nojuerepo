from datetime import date
from typing import List

import model
import db
from acme.model import Event

TITLE_LIMIT = 30
TEXT_LIMIT = 200


class LogicException(Exception):
    pass


class EventAlreadyExistsException(Exception):
    ...


class EventLogic:
    def __init__(self):
        self._event_db = db.EventDB()

    def _validate_event(self, event: model.Event):
        if event is None:
            raise LogicException("Event is None")
        if event.title is None or len(event.title) > TITLE_LIMIT:
            raise LogicException(f"title lenght > MAX: {TITLE_LIMIT}")
        if event.text is None or len(event.text) > TEXT_LIMIT:
            raise LogicException(f"text lenght > MAX: {TEXT_LIMIT}")
        try:
            existing_event = self.get(event.date)
            if existing_event is not None:
                raise EventAlreadyExistsException(f"Event already exists: {event.date}")
        except LogicException:
            pass

    def create(self, event: model.Event) -> str:
        self._validate_event(event)
        try:
            return self._event_db.create(event)
        except Exception as ex:
            raise LogicException(f"failed CREATE operation with: {ex}")

    def get_all(self) -> list[Event]:
        try:
            return self._event_db.get_all()
        except Exception as ex:
            raise LogicException(f"failed LIST operation with: {ex}")

    def get(self, _id: date) -> model.Event:
        try:
            return self._event_db.get(_id)
        except Exception as ex:
            raise LogicException(f"failed READ operation with: {ex}")

    def update(self, _id: str, event: model.Event):
        self._validate_event(event)
        try:
            return self._event_db.update(_id, event)
        except Exception as ex:
            raise LogicException(f"failed UPDATE operation with: {ex}")

    def delete(self, _id: str):
        try:
            return self._event_db.delete(_id)
        except Exception as ex:
            raise LogicException(f"failed DELETE operation with: {ex}")
