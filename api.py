from flask import Flask
from flask import request

app = Flask(__name__)


import model
import logic
from datetime import datetime
_event_logic = logic.EventLogic()


class ApiException(Exception):
    pass


def _from_raw(raw_event: str) -> model.Event:
    parts = raw_event.split('|')
    if len(parts) == 3:
        event = model.Event()
        event.date = datetime.strptime(parts[0], '%Y-%m-%d').date()
        event.title = parts[1]
        event.text = parts[2]
        return event
    elif len(parts) == 4:
        event = model.Event()
        event.date = datetime.strptime(parts[1], '%Y-%m-%d').date()
        event.title = parts[2]
        event.text = parts[3]
        return event
    else:
        raise ApiException(f"invalid RAW note data {raw_event}")


def _to_raw(event: model.Event) -> str:
    return f"{event.id}|{event.date.isoformat()}|{event.title}|{event.text}"


API_ROOT = "/api/v1/calendar/"
EVENT_API_ROOT = API_ROOT + "/event"


@app.route(EVENT_API_ROOT + "/", methods=["POST"])
def create():
    try:
        data = request.get_data().decode('utf-8')
        event = _from_raw(data)
        _id = _event_logic.create(event)
        return f"new id: {_id}", 201
    except Exception as ex:
        return f"failed to CREATE with: {ex}", 404


@app.route(EVENT_API_ROOT + "/", methods=["GET"])
def get_all():
    try:
        events = _event_logic.get_all()
        raw_events = ""
        for event in events:
            raw_events += _to_raw(event) + '\n'
        return raw_events, 200
    except Exception as ex:
        return f"failed to LIST with: {ex}", 404


@app.route(EVENT_API_ROOT + "/<date>/", methods=["GET"])
def get(date: str):
    try:
        parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
        event = _event_logic.get(parsed_date)
        raw_event = _to_raw(event)
        return raw_event, 200
    except Exception as ex:
        return f"failed to READ with: {ex}", 404


@app.route(EVENT_API_ROOT + "/<date>/", methods=["PUT"])
def update(date: str):
    try:
        data = request.get_data().decode('utf-8')
        note = _from_raw(data)
        _event_logic.update(date, note)
        return "updated", 200
    except Exception as ex:
        return f"failed to UPDATE with: {ex}", 404


@app.route(EVENT_API_ROOT + "/<date>/", methods=["DELETE"])
def delete(date: str):
    try:
        _event_logic.delete(date)
        return "deleted", 200
    except Exception as ex:
        return f"failed to DELETE with: {ex}", 404
