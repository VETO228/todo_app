import sqlite3

# Открываем новое соединение (или используем старое)
conn = sqlite3.connect('mybase.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER DEFAULT 0
    )
''')
conn.commit()
print("Таблица products создана!")

# Добавляем нескольких продуктов
# products = [
#     ('Яблоки', 50, 100),
#     ('Бананы', 80, 50),
#     ('Молоко', 70, 30),
#     ('Хлеб', 40, 0),
#     ('Сыр', 150, 20),
# ]
# cursor.executemany('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', products)

# conn.commit()
# Получаем всех продукты
# cursor.execute('SELECT * FROM products')
# all_products = cursor.fetchall()

# print("\n--- Все продукты ---")
# for product in all_products:
#     print(f"id: {product[0]}, товар: {product[1]}, цена: {product[2]}, кол-во: {product[3]}")

# # Получаем продукты меньше 100 руб
# cursor.execute('SELECT * FROM products WHERE price < 100')
# products_price = cursor.fetchall()

# print("------------Продукты меньше 100 руб-----------")
# for product in products_price:
#     print(f"id: {product[0]}, товар: {product[1]}, цена: {product[2]}, кол-во: {product[3]}")

# cursor.execute('UPDATE products SET price = price + 10')
# conn.commit()

# cursor.execute('SELECT * FROM products')
# updated_product = cursor.fetchall()

# print("\n--- После изменения ---")
# for product in updated_product:
#     print(f"id: {product[0]}, товар: {product[1]}, цена: {product[2]}")

# # Удаляем продукт с id = 2
# cursor.execute('DELETE FROM products WHERE id = ?', (2,))
# conn.commit()

# # Проверяем результат
# cursor.execute('SELECT * FROM products')
# remaining_products = cursor.fetchall()

# print("\n--- После удаления id=2 ---")
# for product in remaining_products:
#     print(f"id: {product[0]}, товар: {product[1]}, цена: {product[2]}")

# cursor.execute('ALTER TABLE products ADD COLUMN category TEXT DEFAULT "другое"')
cursor.execute('UPDATE products SET category = "выпечка" WHERE id = 5')
conn.commit()

# Проверяем результат
cursor.execute('SELECT * FROM products')
remaining_products = cursor.fetchall()

print("\n--- После изменения ---")
for product in remaining_products:
    print(f"id: {product[0]}, товар: {product[1]}, цена: {product[2]}, категория: {product[4]}")

# Закрываем соединение
conn.close()
print("\nСоединение закрыто.")