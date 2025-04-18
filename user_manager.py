from getpass import getpass
from models import mysql_db, User

def register_user():
    print("Регистрация пользователя")
    username = input("Имя пользователя: ")
    password = getpass("Пароль: ")
    role = input("Роль (admin / agent): ").lower()

    if role not in ('admin', 'agent'):
        print("Неверная роль. Пользователь не создан.")
        return

    try:
        User.create(username=username, password=password, role=role)
        print("Пользователь успешно зарегистрирован.\n")
    except:
        print("Ошибка: пользователь с таким именем уже существует.\n")

def login():
    print("Вход")
    username = input("Имя пользователя: ")
    password = getpass("Пароль: ")

    try:
        user = User.get(User.username == username)
        if user.password == password:
            print(f"Добро пожаловать, {user.username}! Ваша роль: {user.role}")
            return user
        else:
            print("еверный пароль.")
    except User.DoesNotExist:
        print("Пользователь не найден.")
    return None

def list_users(current_user):
    if current_user.role != 'admin':
        print("Только администраторы могут просматривать список пользователей.\n")
        return

    print("Список пользователей:")
    for user in User.select():
        print(f"{user.id}. {user.username} ({user.role})")
    print()

def menu():
    mysql_db.connect()
    current_user = None
    while True:
        print("""\n=== Меню пользователя ===
1. Регистрация
2. Вход
3. Список пользователей
0. Выход""")
        choice = input("Выберите действие: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            current_user = login()
        elif choice == '3':
            if current_user:
                list_users(current_user)
            else:
                print("Сначала выполните вход.")
        elif choice == '0':
            break
        else:
            print("Неверный выбор.\n")

if __name__ == '__main__':
    menu()
