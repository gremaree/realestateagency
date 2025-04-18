from models import mysql_db, Deal, DealParticipant, DealRealEstate, Client, Agent, RealEstate
from auth_utils import login

def list_clients():
    for c in Client.select():
        fio = c.personal_data.fio
        print(f"{c.id}. {fio.last_name} {fio.first_name}")

def list_agents():
    for a in Agent.select():
        fio = a.personal_data.fio
        print(f"{a.id}. {fio.last_name} {fio.first_name} ({a.specialization})")

def list_real_estates():
    for r in RealEstate.select():
        addr = r.address
        print(f"{r.id}. {addr.city}, {addr.street}, {addr.house_number} ({r.status})")

def create_deal():
    print("\n🔹 Создание сделки")
    process_status = input("Введите статус сделки (в процессе / завершен / отменен): ")
    deal = Deal.create(process_status=process_status)

    print("\nВыберите клиента:")
    list_clients()
    client_id = int(input("ID клиента: "))

    print("\nВыберите агента:")
    list_agents()
    agent_id = int(input("ID агента: "))

    DealParticipant.create(deal=deal, client=client_id, agent=agent_id)

    print("\nВыберите объект недвижимости:")
    list_real_estates()
    real_estate_id = int(input("ID недвижимости: "))
    DealRealEstate.create(deal=deal, real_estate=real_estate_id)

    print("✅ Сделка успешно добавлена.\n")

def list_deals():
    print("\n📋 Список сделок:")
    for deal in Deal.select():
        print(f"Сделка #{deal.id} — статус: {deal.process_status}")
        for part in deal.participants:
            client = part.client.personal_data.fio
            agent = part.agent.personal_data.fio
            print(f"   Клиент: {client.last_name} {client.first_name}")
            print(f"   Агент: {agent.last_name} {agent.first_name}")
        for obj in deal.real_estates:
            addr = obj.real_estate.address
            print(f"   Недвижимость: {addr.city}, {addr.street}, {addr.house_number}")
        print()

def menu():
    user = login()
    if not user:
        return

    while True:
        print("""
=== Меню сделок ===
1. Создать сделку
2. Список сделок
0. Назад""")
        choice = input("Выберите действие: ")
        if choice == '1':
            if user.role in ['admin', 'agent']:
                create_deal()
            else:
                print("⛔ У вас нет прав на создание сделок.\n")
        elif choice == '2':
            list_deals()
        elif choice == '0':
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.\n")

if __name__ == '__main__':
    mysql_db.connect()
    menu()
