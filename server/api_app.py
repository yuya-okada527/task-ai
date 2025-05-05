from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from storage import load_events_from_file
from models import replay_task

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
