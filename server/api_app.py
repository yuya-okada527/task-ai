from fastapi import FastAPI
from storage import load_events_from_file
from models import replay_task

app = FastAPI()


@app.get("/api/tasks")
def list_tasks():
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
