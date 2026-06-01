from flask import Flask, render_template, request, redirect
from database import init_db, get_all_messages, add_messages
from datetime import date

app = Flask(__name__)

# Инициализируем базу данных при запуске приложения
# Вызываем функцию init_db(), которая создаёт таблицу messages, если её ещё нет
# Это происходит один раз при старте сервера
init_db()

@app.route('/')
def index():
    messages = get_all_messages()
    return render_template('index.html', messages=messages)


@app.route('/add', methods=['POST'])
def add_message():
    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()
    if name and message:
        item = add_messages(name, message, date.today().strftime('%Y-%m-%d'))
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)