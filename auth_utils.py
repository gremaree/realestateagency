from getpass import getpass
from models import User, mysql_db

def login():
    mysql_db.connect(reuse_if_open=True)
    print("\nАвторизация")
    username = input("Имя пользователя: ")
    password = getpass("Пароль: ")

    try:
        user = User.get(User.username == username)
        if user.password == password:
            print(f"Добро пожаловать, {user.username}! Ваша роль: {user.role}\n")
            return user
        else:
            print("Неверный пароль.\n")
    except User.DoesNotExist:
        print("Пользователь не найден.\n")
    return None
