from enum import Enum
from typing import List, Dict, Any
import uuid
import json

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Task AI DEMO", debug=True)

# Task Status Enum
class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

# Task Model
class Task:
    def __init__(self, id: str, title: str, description: str, status: TaskStatus = TaskStatus.TODO):
        self.id = id
        self.title = title
        self.description = description
        self.status = status

# Event Model
class Event:
    def __init__(self, event_type: str, task_id: str, payload: Dict[str, Any]):
        self.event_id = str(uuid.uuid4())
        self.event_type = event_type
        self.task_id = task_id
        self.payload = payload

# In-memory Event Store
event_store: Dict[str, List[Event]] = {}


def replay_task(task_id: str) -> Task:
    if task_id not in event_store:
        raise ValueError("Task not found")
    
    # Replay the events to reconstruct the task
    events = event_store[task_id]
    task = Task(id=task_id, title="", description="", status=TaskStatus.TODO)

    for event in events:
        if event.event_type == "TaskCreated":
            task.title = event.payload["title"]
            task.description = event.payload["description"]
            task.status = event.payload["status"]
        elif event.event_type == "TaskUpdated":
            task.title = event.payload["after"]["title"]
            task.description = event.payload["after"]["description"]
            task.status = event.payload["after"]["status"]

    return task


@mcp.tool()
def create_task(title: str, description: str) -> Dict[str, Any]:

    task_id = str(uuid.uuid4())

    # Log the event
    event = Event(event_type="TaskCreated", task_id=task_id, payload={
        "title": title,
        "description": description,
        "status": TaskStatus.TODO
    })
    event_store[task_id] = event_store.get(task_id, []) + [event]

    return {"task_id": task_id}

@mcp.tool()
def update_task(task_id: str, title: str, description: str, status: TaskStatus) -> Dict[str, Any]:
    before_task = replay_task(task_id)

    # Log the event
    event = Event(event_type="TaskUpdated", task_id=task_id, payload={
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
    })
    event_store[task_id] = event_store.get(task_id, []) + [event]

    return {"task_id": task_id}


@mcp.tool()
def list_tasks() -> Dict[str, List[Dict[str, Any]]]:
    tasks = []
    for task_id, events in event_store.items():
        task = replay_task(task_id)
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
    task = replay_task(task_id)
    events = event_store.get(task_id, [])

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
    print("Starting MCP server in stdio mode")
    mcp.run(transport="sse")
