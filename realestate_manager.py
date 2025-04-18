from models import mysql_db, Address, RealEstate, Apartment, House, LandPlot
from auth_utils import login

def create_real_estate():
    print("\nДобавление объекта недвижимости")
    city = input("Город: ")
    street = input("Улица: ")
    house = input("Дом: ")

    area = float(input("Площадь (м²): "))
    cost = float(input("Стоимость: "))
    status = input("Статус (свободен/в аренде/продан): ")
    year = int(input("Год постройки: "))

    addr = Address.create(city=city, street=street, house_number=house)
    real_estate = RealEstate.create(area=area, cost=cost, status=status, year_built=year, address=addr)

    print("Тип объекта:")
    print("1. Квартира")
    print("2. Дом")
    print("3. Земельный участок")
    choice = input("Выберите: ")

    if choice == '1':
        floor = int(input("Этаж: "))
        rooms = int(input("Кол-во комнат: "))
        number = input("Номер квартиры: ")
        Apartment.create(real_estate=real_estate, floor=floor, rooms=rooms, number=number)
    elif choice == '2':
        floors = int(input("Этажность дома: "))
        House.create(real_estate=real_estate, floors=floors)
    elif choice == '3':
        land_type = input("Тип участка: ")
        LandPlot.create(real_estate=real_estate, land_type=land_type)
    else:
        print("Неверный выбор. Объект создан как общая недвижимость.")

    print("Недвижимость успешно добавлена.\n")

def list_real_estates():
    print("\nСписок объектов недвижимости:")
    for obj in RealEstate.select():
        addr = obj.address
        print(f"{obj.id}. {addr.city}, {addr.street}, {addr.house_number} — {obj.area}м², {obj.status}, {obj.cost} руб.")
    print()

def menu():
    user = login()
    if not user:
        return

    while True:
        print("""
=== Меню недвижимости ===
1. Добавить объект
2. Список объектов
0. Назад""")
        choice = input("Выберите действие: ")
        if choice == '1':
            if user.role == 'admin':
                create_real_estate()
            else:
                print("Только администратор может добавлять объекты.\n")
        elif choice == '2':
            list_real_estates()
        elif choice == '0':
            break
        else:
            print("Неверный выбор. Попробуйте снова.\n")

if __name__ == '__main__':
    mysql_db.connect()
    menu()
