from flask import Flask, render_template, request, redirect, session
from database import init_db, get_all_messages, add_messages, delete_messages, get_message_count, delete_all_messages, check_user, reg_user
from datetime import date

app = Flask(__name__)

# Инициализируем базу данных при запуске приложения
# Вызываем функцию init_db(), которая создаёт таблицу messages, если её ещё нет
# Это происходит один раз при старте сервера
init_db()
app.secret_key = 'секретный_ключ_для_гостевой_книги_12345'


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    name = request.form.get('name', '').strip()
    password = request.form.get('password', '').strip()
    if name and password:
        item = reg_user(name, password)
        return redirect('/login')
    return render_template('reg.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Страница входа в приложение.
    GET — показывает форму входа.
    POST — обрабатывает отправленные логин и пароль.
    """
    error = None  # переменная для сообщения об ошибке
    
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Проверяем, правильные ли логин и пароль
        if check_user(username, password):
            # Сохраняем информацию о входе в сессию
            # session — это словарь, который хранится на сервере
            # данные привязаны к конкретному браузеру через cookies
            session['logged_in'] = True   # флаг, что пользователь вошёл
            session['username'] = username  # сохраняем имя пользователя
            return redirect('/')  # перенаправляем на главную
        else:
            error = 'Неверный логин или пароль'
    
    # GET-запрос или ошибка — показываем форму входа
    return render_template('login.html', error=error)


@app.route('/')
def index():
    messages = get_all_messages()
    total_count = get_message_count()
    today = date.today().isoformat()
    return render_template(
        'index.html', messages=messages, total_count=total_count, today=today,
        logged_in=session.get('logged_in', False),  # по умолчанию False
        username=session.get('username')  # имя пользователя или None
    )


@app.route('/logout')
def logout():
    """
    Выход из приложения.
    Удаляет данные пользователя из сессии.
    """
    # pop удаляет ключ из словаря session
    # Если ключа нет, ничего не происходит
    session.pop('logged_in', None)
    session.pop('username', None)
    
    # Перенаправляем на главную страницу
    return redirect('/')


@app.route('/add', methods=['POST'])
def add_message():
    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()
    if name and message:
        item = add_messages(name, message, date.today().strftime('%Y-%m-%d'))
    return redirect("/")


@app.route('/delete/<int:item_id>')
def delete_message(item_id):
    if not session.get('logged_in'):
        return redirect('/login')
    delete_messages(item_id)
    return redirect("/")


@app.route('/delete_all/', methods=['GET'])
def delete_all_get():
    return render_template("delete_all.html")


@app.route('/delete-all-confirm', methods=['POST'])
def delete_all():
    delete_all_messages()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)