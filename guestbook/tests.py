import pytest
import sqlite3
from app import app
from database import check_user


def test_index():
    """Главная страница должна открываться."""
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert 'Гостевая книга'.encode('utf-8') in response.data


def test_add_message():
    """После отправки формы сообщение должно появиться."""
    client = app.test_client()
    
    # Отправляем форму
    client.post('/add', data={
        'name': 'Тест',
        'message': 'Привет!'
    })
    
    # Проверяем, что сообщение появилось на главной
    response = client.get('/')
    assert 'Тест'.encode('utf-8') in response.data
    assert 'Привет!'.encode('utf-8') in response.data


def test_login_page():
    """Страница входа должна содержать форму."""
    client = app.test_client()
    response = client.get('/login')
    assert response.status_code == 200
    assert 'Вход'.encode('utf-8') in response.data
    assert 'username'.encode('utf-8') in response.data


def test_login_success():
    client = app.test_client()
    # В тесте мы отправляем логин и пароль
    client.post('/login', data={'username': 'admin', 'password': '123'})

    # Затем проверяем сессию
    with client.session_transaction() as sess:
        assert sess.get('logged_in') is True
        assert sess.get('username') == 'admin'


def test_login_failure():
    client = app.test_client()
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'wrong'
    })

    # Проверяем, что есть сообщение об ошибке
    assert 'Неверный логин или пароль'.encode('utf-8') in response.data

    # Проверяем, что сессия НЕ установлена
    with client.session_transaction() as sess:
        assert sess.get('logged_in') is None


def test_delete_without_auth():
    client = app.test_client()
    # Отправляем запрос на удаление без авторизации
    response = client.get('/delete/1')

    # Должен быть редирект на /login
    assert response.status_code == 302


def test_delete_with_auth():
    client = app.test_client()
    # Входим
    client.post('/login', data={'username': 'admin', 'password': '123'})

    # Добавляем сообщение
    client.post('/add', data={'name': 'Тест', 'message': 'Сообщение'})

    # Удаляем
    response = client.get('/delete/1')
    assert response.status_code == 302  # редирект на главную

    # Проверяем, что сообщение исчезло
    response = client.get('/')
    assert 'Сообщение для удаления'.encode('utf-8') not in response.data


def test_logout():
    client = app.test_client()
    # Сначала входим
    client.post('/login', data={
        'username': 'admin',
        'password': '123'
    })
    
    # Проверяем, что вошли
    with client.session_transaction() as sess:
        assert sess.get('logged_in') is True
    
    # Выходим
    client.get('/logout')
    
    # Проверяем, что вышли
    with client.session_transaction() as sess:
        assert sess.get('logged_in') is None
        assert sess.get('username') is None


def test_user_creation():
    assert check_user("admin", 123) == True
    assert check_user("vadim", 111) == True
    assert check_user("qwerty", 1) == False
    
