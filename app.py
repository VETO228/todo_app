from datetime import datetime
import json
import os

from flask import Flask, redirect, render_template, request


app = Flask(__name__)
FILE_NAME = "tasks.json"


def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    return []


def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


tasks = load_tasks()


@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    text = request.form.get("task", "").strip()
    if text:
        tasks.append(
            {
                "text": text,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        )
        save_tasks(tasks)
    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect("/")


@app.route("/clear")
def clear_tasks():
    tasks.clear()
    save_tasks(tasks)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
