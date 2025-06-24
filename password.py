import sqlite3
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

conn = sqlite3.connect('passwords.db')
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