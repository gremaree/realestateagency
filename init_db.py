from peewee import *
from models import (
    mysql_db, FIO, PassportData, Address, PersonalData,
    Client, Agent, RealEstate, LandPlot, House, Apartment,
    Deal, DealParticipant, DealRealEstate, Contract, Sale, Rent, User
)

def create_tables():
    with mysql_db:
        mysql_db.create_tables([
            FIO, PassportData, Address, PersonalData,
            Client, Agent, RealEstate, LandPlot, House, Apartment,
            Deal, DealParticipant, DealRealEstate, Contract, Sale, Rent, User
        ])
    print("Таблицы успешно созданы.")

if __name__ == '__main__':
    create_tables()
