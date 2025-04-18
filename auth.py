from getpass import getpass
from models import User, mysql_db

def login():
    mysql_db.connect(reuse_if_open=True)
    print("Вход")
    username = input("Имя пользователя: ")
    password = getpass("Пароль: ")

    try:
        user = User.get(User.username == username)
        if user.password == password:
            print(f"Авторизация успешна. Роль: {user.role}")
            return user
        else:
            print("Неверный пароль.")
    except User.DoesNotExist:
        print("Пользователь не найден.")
    return None
