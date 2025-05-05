# storage.py
import json
import os
from typing import List, Dict
from models import Event

# File path for the event store
EVENT_STORE_FILE = "storage/event_store.json"

# Load events from the file if it exists
def load_events_from_file() -> Dict[str, List[Event]]:
    if os.path.exists(EVENT_STORE_FILE):
        with open(EVENT_STORE_FILE, "r") as file:
            raw_events = json.load(file)
            # Convert raw JSON data to Event objects
            return {
                task_id: [
                    Event(
                        event_id=event["event_id"],
                        event_type=event["event_type"],
                        task_id=event["task_id"],
                        payload=event["payload"]
                    ) for event in events
                ] for task_id, events in raw_events.items()
            }
    return {}

# Save events to the file
def save_event_to_file(event):
    all_events = load_events_from_file()
    task_id = event.task_id
    if task_id not in all_events:
        all_events[task_id] = []
    all_events[task_id].append(event)
    # Convert Event objects to dictionaries for JSON serialization
    serializable_events = {
        task_id: [
            {
                "event_id": e.event_id,
                "event_type": e.event_type,
                "task_id": e.task_id,
                "payload": e.payload
            } for e in events
        ] for task_id, events in all_events.items()
    }
    with open(EVENT_STORE_FILE, "w") as file:
        json.dump(serializable_events, file, indent=4)