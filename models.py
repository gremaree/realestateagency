from peewee import *

# Подключение к MySQL
mysql_db = MySQLDatabase(
    'realestateagency', user='root', password='Perrol', host='127.0.0.1', port=3306
)

class BaseModel(Model):
    class Meta:
        database = mysql_db

# ------------------- Персональные данные -------------------
class FIO(BaseModel):
    last_name = CharField()
    first_name = CharField()
    patronymic = CharField(null=True)

class PassportData(BaseModel):
    series = CharField(max_length=10)
    number = CharField(max_length=20)

class Address(BaseModel):
    city = CharField()
    street = CharField()
    house_number = CharField()

class PersonalData(BaseModel):
    fio = ForeignKeyField(FIO, backref='personal_data')
    passport = ForeignKeyField(PassportData, backref='personal_data')
    address = ForeignKeyField(Address, backref='personal_data')

# ------------------- Клиенты и агенты -------------------
class Client(BaseModel):
    personal_data = ForeignKeyField(PersonalData, backref='clients')

class Agent(BaseModel):
    personal_data = ForeignKeyField(PersonalData, backref='agents')
    specialization = CharField()
    salary = DecimalField(max_digits=10, decimal_places=2)

# ------------------- Недвижимость -------------------
class RealEstate(BaseModel):
    area = DecimalField(max_digits=10, decimal_places=2)
    cost = DecimalField(max_digits=15, decimal_places=2)
    status = CharField()
    year_built = IntegerField()
    address = ForeignKeyField(Address, backref='real_estate')

class LandPlot(BaseModel):
    real_estate = ForeignKeyField(RealEstate, backref='land_plot')
    land_type = CharField()

class House(BaseModel):
    real_estate = ForeignKeyField(RealEstate, backref='house')
    floors = IntegerField()

class Apartment(BaseModel):
    real_estate = ForeignKeyField(RealEstate, backref='apartment')
    floor = IntegerField()
    rooms = IntegerField()
    number = CharField()

# ------------------- Сделки -------------------
class Deal(BaseModel):
    process_status = CharField()

class DealParticipant(BaseModel):
    deal = ForeignKeyField(Deal, backref='participants')
    client = ForeignKeyField(Client, backref='deals')
    agent = ForeignKeyField(Agent, backref='deals')

class DealRealEstate(BaseModel):
    deal = ForeignKeyField(Deal, backref='real_estates')
    real_estate = ForeignKeyField(RealEstate, backref='deals')

# ------------------- Договоры -------------------
class Contract(BaseModel):
    deal = ForeignKeyField(Deal, backref='contracts')
    number = CharField()

class Sale(BaseModel):
    contract = ForeignKeyField(Contract, backref='sale')
    date = DateField()

class Rent(BaseModel):
    contract = ForeignKeyField(Contract, backref='rent')
    start_date = DateField()
    end_date = DateField()
    monthly_rate = DecimalField(max_digits=10, decimal_places=2)

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    role = CharField(choices=[('admin', 'admin'), ('agent', 'agent')])
