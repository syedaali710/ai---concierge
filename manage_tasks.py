# manage_tasks.py

tasks = []

def manage_tasks(action: str, task=None):
    if action == "add" and task:
        tasks.append(task)
        return {"message": f"Task added: {task['title']}"}
    elif action == "list":
        return {"tasks": tasks}
    else:
        return {"error": "Invalid action or missing task"}

# Example usage
if __name__ == "__main__":
    print(manage_tasks("add", {
        "title": "AI Demo Call",
        "when": "Thursday 3:00 PM",
        "description": "Demo of AI Concierge"
    }))
    print(manage_tasks("list"))
