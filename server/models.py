from enum import Enum
from typing import Dict, Any

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
    def __init__(self, event_id: str, event_type: str, task_id: str, payload: Dict[str, Any]):
        self.event_id = event_id
        self.event_type = event_type
        self.task_id = task_id
        self.payload = payload