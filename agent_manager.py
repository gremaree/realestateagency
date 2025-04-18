from models import mysql_db, FIO, PassportData, Address, PersonalData, Agent
from auth_utils import login

def create_agent():
    print("\n🔹 Добавление нового агента")
    last = input("Фамилия: ")
    first = input("Имя: ")
    patronymic = input("Отчество (необязательно): ")

    series = input("Серия паспорта: ")
    number = input("Номер паспорта: ")

    city = input("Город: ")
    street = input("Улица: ")
    house = input("Дом: ")

    specialization = input("Специализация: ")
    salary = float(input("Зарплата: "))

    fio = FIO.create(last_name=last, first_name=first, patronymic=patronymic or None)
    passport = PassportData.create(series=series, number=number)
    address = Address.create(city=city, street=street, house_number=house)
    pdata = PersonalData.create(fio=fio, passport=passport, address=address)
    Agent.create(personal_data=pdata, specialization=specialization, salary=salary)

    print("✅ Агент успешно добавлен.\n")

def list_agents():
    print("\n📋 Список агентов:")
    for agent in Agent.select():
        fio = agent.personal_data.fio
        print(f"{agent.id}. {fio.last_name} {fio.first_name} ({agent.specialization}) — {agent.salary} руб.")
    print()

def delete_agent():
    list_agents()
    agent_id = int(input("Введите ID агента для удаления: "))
    try:
        agent = Agent.get_by_id(agent_id)
        agent.delete_instance(recursive=True)
        print("🗑️ Агент удалён.\n")
    except Agent.DoesNotExist:
        print("Агент с таким ID не найден.\n")

def menu():
    user = login()
    if not user or user.role != 'admin':
        print("Доступ запрещён. Только администраторы могут управлять агентами.\n")
        return

    while True:
        print("""
=== Меню управления агентами ===
1. Добавить агента
2. Список агентов
3. Удалить агента
0. Выход""")
        choice = input("Выберите действие: ")
        if choice == '1':
            create_agent()
        elif choice == '2':
            list_agents()
        elif choice == '3':
            delete_agent()
        elif choice == '0':
            break
        else:
            print("Неверный выбор. Попробуйте снова.\n")

if __name__ == '__main__':
    mysql_db.connect()
    menu()
