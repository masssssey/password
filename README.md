# password
import sqlite3Add commentMore actions
import hashlib
import os
import random
import string

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    pwd_hash = hashlib.sha256(salt + password.encode()).hexdigest()
    return pwd_hash, salt

def verify_password(stored_hash, salt, password_to_check):
    check_hash, _ = hash_password(password_to_check, salt)
    return stored_hash == check_hash

conn = sqlite3.connect('passwords.db')Add commentMore actions
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, hash TEXT, salt BLOB)''')

password = generate_password()
hash_val, salt = hash_password(password)
c.execute('INSERT INTO passwords (hash, salt) VALUES (?, ?)', (hash_val, salt))
conn.commit()
print(f"Сгенерированный пароль: {password}")

c.execute('SELECT hash, salt FROM passwords ORDER BY id DESC LIMIT 1')
row = c.fetchone()
if row:
    stored_hash, stored_salt = row[0], row[1]
    check = verify_password(stored_hash, stored_salt, password)
    print("Пароль успешно проверен!" if check else "Ошибка проверки пароля!")

conn.close()
# Объяснение
1. Импортируем необходимые модули:
sqlite3 — для работы с базой данных SQLite.
hashlib — для хэширования паролей с помощью SHA-256.
os — для генерации случайной соли.
random и string — для генерации случайного пароля.

2. Функция генерации пароля def generate_password(length=12): chars = string.ascii_letters + string.digits + string.punctuation return ''.join(random.choice(chars) for _ in range(length))
Создаёт случайный пароль длиной по умолчанию 12 символов.
Использует буквы (заглавные и строчные), цифры и знаки пунктуации.
Каждый символ выбирается случайно из набора.

3. Функция хэширования пароля с солью def hash_password(password, salt=None): if salt is None: salt = os.urandom(16) # Генерируем случайную 16-байтовую соль pwd_hash = hashlib.sha256(salt + password.encode()).hexdigest() return pwd_hash, salt
Если соль не передана, генерируется новая случайная соль длиной 16 байт.
Хэшируется конкатенация соли и пароля (пароль преобразуется в байты).
Используется алгоритм SHA-256.
Возвращается хэш в шестнадцатеричном виде и соль (в байтах).

4. Функция проверки пароля def verify_password(stored_hash, salt, password_to_check): check_hash, _ = hash_password(password_to_check, salt) return stored_hash == check_hash
Принимает сохранённый хэш, соль и пароль для проверки.
Хэширует переданный пароль с той же солью.
Сравнивает полученный хэш с сохранённым.
Возвращает True, если совпадают, иначе False.

5. Работа с базой данных SQLite conn = sqlite3.connect('passwords.db') c = conn.cursor() c.execute('''CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, hash TEXT, salt BLOB)''')
Подключается к базе данных passwords.db (создаётся, если не существует).
Создаёт таблицу passwords, если она ещё не создана, с тремя полями:
id — уникальный идентификатор (автоинкремент).
hash — хэш пароля (текст).
salt — соль (хранится как BLOB).

6. Генерация пароля и запись в базу password = generate_password() hash_val, salt = hash_password(password) c.execute('INSERT INTO passwords (hash, salt) VALUES (?, ?)', (hash_val, salt)) conn.commit() print(f"Сгенерированный пароль: {password}")
Генерируется новый пароль.
Пароль хэшируется вместе с солью.
Хэш и соль записываются в таблицу.
Сохраняются изменения.
Выводится сгенерированный пароль.

7. Проверка пароля из базы c.execute('SELECT hash, salt FROM passwords ORDER BY id DESC LIMIT 1') row = c.fetchone() if row: stored_hash, stored_salt = row[0], row[1] check = verify_password(stored_hash, stored_salt, password) print("Пароль успешно проверен!" if check else "Ошибка проверки пароля!")
Извлекается последний добавленный хэш и соль из базы.
Если запись найдена, вызывается функция проверки пароля.
Выводится сообщение об успешной или неуспешной проверке.

8. Закрытие соединения с базой conn.close()
