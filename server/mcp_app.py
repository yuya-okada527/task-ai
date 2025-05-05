from enum import Enum
from typing import List, Dict, Any
import uuid
import json
import os

from mcp.server.fastmcp import FastMCP
from models import TaskStatus, Task, Event, replay_task
from storage import load_events_from_file, save_event_to_file

mcp = FastMCP("Task AI DEMO", debug=True)

@mcp.tool()
def create_task(title: str, description: str) -> Dict[str, Any]:

    task_id = str(uuid.uuid4())

    # Log the event
    event = Event(
        event_id=str(uuid.uuid4()),
        event_type="TaskCreated",
        task_id=task_id,
        payload={
            "title": title,
            "description": description,
            "status": TaskStatus.TODO
        }
    )
    save_event_to_file(event)

    return {"task_id": task_id}

@mcp.tool()
def update_task(task_id: str, title: str, description: str, status: TaskStatus) -> Dict[str, Any]:
    events = load_events_from_file().get(task_id, [])
    before_task = replay_task(events)

    # Log the event
    event = Event(
        event_id=str(uuid.uuid4()),
        event_type="TaskUpdated",
        task_id=task_id,
        payload={
            "before": {
                "title": before_task.title,
                "description": before_task.description,
                "status": before_task.status
            },
            "after": {
                "title": title,
                "description": description,
                "status": status
            }
        }
    )
    save_event_to_file(event)

    return {"task_id": task_id}


@mcp.tool()
def list_tasks() -> Dict[str, List[Dict[str, Any]]]:
    tasks = []
    event_store = load_events_from_file()
    for task_id, events in event_store.items():
        task = replay_task(event_store.get(task_id, []))
        tasks.append(task)
    return {
        "tasks": [
            {
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status
            } for task in tasks
        ]
    }


@mcp.tool()
def get_task(task_id: str) -> Dict[str, Any]:
    event_store = load_events_from_file()
    events = event_store.get(task_id, [])
    task = replay_task(events)

    # Retrieve task history
    history = [
        {
            "event_id": event.event_id,
            "message": f"{event.event_type} event occurred",
            "payload": event.payload
        }
        for event in events
    ]

    return {
        "task_id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "history": history
    }

def main():
    print("Server is running...")

    # Example usage
    example_task = create_task("Example Task", "This is an example task.")
    print(json.dumps(example_task, indent=4))

    updated_task = update_task(
        example_task["task_id"], "Updated Task", "Updated description", TaskStatus.IN_PROGRESS
    )
    print(json.dumps(updated_task, indent=4))

    all_tasks = list_tasks()
    print(json.dumps(all_tasks, indent=4))

    task_details = get_task(example_task["task_id"])
    print(json.dumps(task_details, indent=4))

if __name__ == "__main__":
    is_test_mode = os.getenv("IS_TEST_MODE", "false").lower() == "true"
    if is_test_mode:
        main()
    else:
        print("Starting MCP server in stdio mode")
        mcp.run(transport="sse")
