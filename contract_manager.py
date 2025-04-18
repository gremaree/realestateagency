from models import mysql_db, Contract, Sale, Rent, Deal
from auth_utils import login

def list_deals():
    print("\n📋 Сделки:")
    for d in Deal.select():
        print(f"{d.id}. Статус: {d.process_status}")

def create_contract():
    print("\n🔹 Создание договора")
    list_deals()
    deal_id = int(input("Введите ID сделки: "))
    number = input("Номер договора: ")

    contract = Contract.create(deal=deal_id, number=number)

    print("Тип договора:")
    print("1. Продажа")
    print("2. Аренда")
    choice = input("Выберите: ")

    if choice == '1':
        date = input("Дата продажи (ГГГГ-ММ-ДД): ")
        Sale.create(contract=contract, date=date)
        print("✅ Договор продажи добавлен.")
    elif choice == '2':
        start = input("Дата начала аренды (ГГГГ-ММ-ДД): ")
        end = input("Дата окончания аренды (ГГГГ-ММ-ДД): ")
        rate = float(input("Месячная ставка аренды: "))
        Rent.create(contract=contract, start_date=start, end_date=end, monthly_rate=rate)
        print("✅ Договор аренды добавлен.")
    else:
        print("❌ Неверный тип. Договор добавлен без условий.")

def list_contracts():
    print("\n📋 Договоры:")
    for c in Contract.select():
        print(f"\nДоговор #{c.id} ({c.number}) — сделка #{c.deal.id}")
        if hasattr(c, 'sale'):
            print(f"  Тип: Продажа | Дата: {c.sale.date}")
        elif hasattr(c, 'rent'):
            print(f"  Тип: Аренда | Срок: {c.rent.start_date} — {c.rent.end_date} | {c.rent.monthly_rate} руб./мес")
        else:
            print("  ❓ Без условий")

def menu():
    user = login()
    if not user or user.role != 'admin':
        print("⛔ Доступ запрещён. Только администраторы могут управлять договорами.\n")
        return

    while True:
        print("""
=== Меню договоров ===
1. Создать договор
2. Список договоров
0. Назад""")
        choice = input("Выберите действие: ")
        if choice == '1':
            create_contract()
        elif choice == '2':
            list_contracts()
        elif choice == '0':
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.\n")

if __name__ == '__main__':
    mysql_db.connect()
    menu()
