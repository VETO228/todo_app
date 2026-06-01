from datetime import datetime
import json
import os
import sqlite3

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
    priority = request.form.get("priority", "средний").strip()
    if text:
        tasks.append(
            {
                "text": text,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "done": False,
                "priority": priority,
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


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if task_id < 0 or task_id >= len(tasks):
        return "Задача не найдена", 404

    if len(tasks[task_id]["text"]) == 0:
        return redirect("/") 

    if request.method == 'POST':
        new_text = request.form.get('task', '').strip()

        if new_text:
            tasks[task_id]['text'] = new_text
            save_tasks(tasks)
        return redirect('/')

    else:
        return render_template('edit.html', task=tasks[task_id])


@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id]['done']
        save_tasks(tasks)
    return redirect('/')

@app.route('/active')
def active_tasks():
    return render_template("active.html", tasks=tasks)


@app.route('/completed')
def completed_tasks():
    return render_template("completed.html", tasks=tasks)


@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    if query:
        filtered_tasks = [task for task in tasks if query in task['text'].lower()]
    else:
        filtered_tasks = tasks
    return render_template('index.html', tasks=filtered_tasks, search_query=query)


@app.route('/sort/date')
def sort_by_date(): 
	# key=lambda t: t.get('date', '') — для каждой задачи берём поле 'date'
 # Если поля 'date' нет, используем пустую строку ''
 # reverse=True — сортируем от большей даты к меньшей (новые сверху)
    sorted_tasks = sorted(tasks, key=lambda t: t.get('date', ''), reverse=True)
    return render_template('index.html', tasks=sorted_tasks)


@app.route('/sort/status')
def sort_by_status():
    # False (не выполнено) идёт раньше True (выполнено)
     # key=lambda t: t.get('done', False) — берём значение 'done' (True или False)
 # В Python False == 0, True == 1, поэтому сначала идут задачи с False
    sorted_tasks = sorted(tasks, key=lambda t: t.get('done', False))
    return render_template('index.html', tasks=sorted_tasks)


@app.route('/sort/priority')
def sort_by_priority():
 # Задаём числовой вес каждому приоритету
 # высокий = 1 (самый маленький, будет первым)
 # средний = 2
 # низкий = 3 (самый большой, будет последним)
    priority_order = {'высокий': 1, 'средний': 2, 'низкий': 3}
# Для каждой задачи:
 # - берём её priority (если нет — 'средний' по умолчанию)
 # - преобразуем в число по словарю priority_order
 # - сортируем по этому числу (от меньшего к большему)
    sorted_tasks = sorted(
        tasks,
        key=lambda t: priority_order.get(t.get('priority', 'средний'), 2)
    )
    return render_template('index.html', tasks=sorted_tasks)


@app.route('/sort/alpha')
def sort_by_alpha():
 # key=lambda t: t.get('text', '').lower() — берём текст задачи
 # .lower() — приводим к нижнему регистру (чтобы А и а не различались)
 # сортируем в алфавитном порядке (A → Z, А → Я)
    sorted_tasks = sorted(tasks, key=lambda t: t.get('text', '').lower())
    return render_template('index.html', tasks=sorted_tasks)


@app.route('/sort/alter_status')
def sort_by_alter_status():
    sorted_tasks = sorted(tasks, key=lambda t: t.get('false', True))
    return render_template('index.html', tasks=sorted_tasks)


@app.route('/products')
def products():
    conn = sqlite3.connect('mybase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template("base.html", products=products)


if __name__ == "__main__":
    app.run(debug=True)