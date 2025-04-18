from models import mysql_db, FIO, PassportData, Address, PersonalData, Client
from auth_utils import login

def create_client():
    print("\n🔹 Создание нового клиента")
    last = input("Фамилия: ")
    first = input("Имя: ")
    patronymic = input("Отчество (необязательно): ")

    series = input("Серия паспорта: ")
    number = input("Номер паспорта: ")

    city = input("Город: ")
    street = input("Улица: ")
    house = input("Дом: ")

    fio = FIO.create(last_name=last, first_name=first, patronymic=patronymic or None)
    passport = PassportData.create(series=series, number=number)
    address = Address.create(city=city, street=street, house_number=house)
    pdata = PersonalData.create(fio=fio, passport=passport, address=address)
    Client.create(personal_data=pdata)
    print("✅ Клиент успешно добавлен.\n")

def list_clients():
    print("\n📋 Список клиентов:")
    for client in Client.select():
        fio = client.personal_data.fio
        addr = client.personal_data.address
        print(f"{client.id}. {fio.last_name} {fio.first_name} {fio.patronymic or ''} — {addr.city}, {addr.street}, {addr.house_number}")
    print()

def delete_client():
    list_clients()
    client_id = int(input("Введите ID клиента для удаления: "))
    try:
        client = Client.get_by_id(client_id)
        client.delete_instance(recursive=True)
        print("🗑️ Клиент удалён.\n")
    except Client.DoesNotExist:
        print("❌ Клиент с таким ID не найден.\n")

def menu():
    user = login()
    if not user or user.role != 'admin':
        print("⛔ Доступ запрещён. Только администраторы могут управлять клиентами.\n")
        return

    while True:
        print("""
=== Меню управления клиентами ===
1. Добавить клиента
2. Список клиентов
3. Удалить клиента
0. Выход""")
        choice = input("Выберите действие: ")
        if choice == '1':
            create_client()
        elif choice == '2':
            list_clients()
        elif choice == '3':
            delete_client()
        elif choice == '0':
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.\n")

if __name__ == '__main__':
    mysql_db.connect()
    menu()
