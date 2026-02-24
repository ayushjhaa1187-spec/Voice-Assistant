import json
import os
import uuid
from datetime import datetime

class TaskAgent:
    def __init__(self, task_file="tasks.json"):
        self.task_file = task_file
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        if not os.path.exists(self.task_file):
            return []
        try:
            with open(self.task_file, "r") as f:
                return json.load(f)
        except:
            return []

    def _save_tasks(self):
        with open(self.task_file, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def execute(self, action: str, **kwargs):
        if action == "add":
            return self.add_task(kwargs.get("description"), kwargs.get("due_date"))
        elif action == "list":
            return self.list_tasks(kwargs.get("status"))
        elif action == "complete":
            return self.complete_task(kwargs.get("task_id"))
        elif action == "delete":
            return self.delete_task(kwargs.get("task_id"))
        return "Unknown action"

    def add_task(self, description: str, due_date: str = None):
        task = {
            "id": str(uuid.uuid4())[:8],
            "description": description,
            "due_date": due_date,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self._save_tasks()
        return f"Task added: {description} (ID: {task['id']})"

    def list_tasks(self, status: str = None):
        filtered_tasks = self.tasks
        if status:
            filtered_tasks = [t for t in self.tasks if t["status"] == status]

        if not filtered_tasks:
            return "No tasks found."

        return "\n".join([f"[{t['id']}] {t['description']} ({t['status']})" for t in filtered_tasks])

    def complete_task(self, task_id: str):
        for t in self.tasks:
            if t["id"] == task_id:
                t["status"] = "completed"
                self._save_tasks()
                return f"Task {task_id} marked as completed."
        return f"Task {task_id} not found."

    def delete_task(self, task_id: str):
        original_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        if len(self.tasks) < original_len:
            self._save_tasks()
            return f"Task {task_id} deleted."
        return f"Task {task_id} not found."
