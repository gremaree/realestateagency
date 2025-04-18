import random
from datetime import date, timedelta
from models import *
from peewee import fn

mysql_db.connect()

def clear_all():
    print("🧹 Очищаем таблицы...")
    Rent.delete().execute()
    Sale.delete().execute()
    Contract.delete().execute()
    DealParticipant.delete().execute()
    Deal.delete().execute()
    Apartment.delete().execute()
    House.delete().execute()
    LandPlot.delete().execute()
    RealEstate.delete().execute()
    Agent.delete().execute()
    Client.delete().execute()
    PersonalData.delete().execute()
    FIO.delete().execute()
    PassportData.delete().execute()
    Address.delete().execute()
    print("✅ Таблицы очищены.")

# Данные для генерации
first_names = ["Иван", "Анна", "Олег", "Мария", "Дмитрий", "Екатерина"]
last_names = ["Иванов", "Смирнова", "Кузнецов", "Попова", "Васильев", "Новикова"]
patronymics = ["Иванович", "Сергеевна", "Петрович", "Алексеевна"]

cities = ["Москва", "Казань", "Санкт-Петербург", "Екатеринбург"]
streets = ["Ленина", "Тверская", "Советская", "Мира", "Пушкина"]

specializations = ["Квартиры", "Загородная", "Коммерческая"]

def create_fio():
    return FIO.create(
        last_name=random.choice(last_names),
        first_name=random.choice(first_names),
        patronymic=random.choice(patronymics)
    )

def create_passport():
    return PassportData.create(
        series=str(random.randint(1000, 9999)),
        number=str(random.randint(100000, 999999))
    )

def create_address():
    return Address.create(
        city=random.choice(cities),
        street=random.choice(streets),
        house_number=str(random.randint(1, 100))
    )

def create_person():
    fio = create_fio()
    passport = create_passport()
    address = create_address()
    return PersonalData.create(fio=fio, passport=passport, address=address)

def create_clients(n=5):
    for _ in range(n):
        Client.create(personal_data=create_person())

def create_agents(n=3):
    for _ in range(n):
        pdata = create_person()
        Agent.create(
            personal_data=pdata,
            specialization=random.choice(specializations),
            salary=random.randint(50000, 100000)
        )

def create_real_estate(n=6):
    for _ in range(n):
        address = create_address()
        t = random.choice(["apartment", "house", "landplot"])
        estate = RealEstate.create(type=t, status=random.choice(["свободен", "в аренде", "продан"]), address=address)
        if t == "apartment":
            Apartment.create(real_estate=estate, floor=random.randint(1, 15), rooms=random.randint(1, 4))
        elif t == "house":
            House.create(real_estate=estate, floors=random.randint(1, 3))
        else:
            LandPlot.create(real_estate=estate, area=random.randint(200, 1200))

def create_real_estate():
    types = ["apartment", "house", "landplot"]
    for t in types:
        for _ in range(2):  # по 2 каждого типа
            address = create_address()
            estate = RealEstate.create(
                type=t,
                status=random.choice(["свободен", "в аренде", "продан"]),
                address=address
            )
            if t == "apartment":
                Apartment.create(real_estate=estate, floor=random.randint(1, 10), rooms=random.randint(1, 4))
            elif t == "house":
                House.create(real_estate=estate, floors=random.randint(1, 3))
            elif t == "landplot":
                LandPlot.create(real_estate=estate, area=random.randint(300, 1500))


def show_summary():
    print("\n📊 Сводка:")
    print(f"👥 Клиенты: {Client.select().count()}")
    print(f"👨‍💼 Агенты: {Agent.select().count()}")
    print(f"🏘 Недвижимость: {RealEstate.select().count()}")
    print(f"🤝 Сделки: {Deal.select().count()}")
    print(f"📄 Договоры: {Contract.select().count()}")
    print(f"🔁 Аренда: {Rent.select().count()} | 💰 Продажа: {Sale.select().count()}")

def generate_all():
    clear_all()
    create_clients(5)
    create_agents(3)
    create_real_estate(6)
    create_deals_and_contracts()
    show_summary()

if __name__ == "__main__":
    mysql_db.connect(reuse_if_open=True)
    generate_all()
