import json
import pandas as pd
from models import *

EXPORT_FOLDER = "exports"

def export_clients():
    data = []
    for c in Client.select():
        fio = c.personal_data.fio
        addr = c.personal_data.address
        passport = c.personal_data.passport
        data.append({
            "id": c.id,
            "ФИО": f"{fio.last_name} {fio.first_name} {fio.patronymic or ''}",
            "Паспорт": f"{passport.series} {passport.number}",
            "Адрес": f"{addr.city}, {addr.street}, {addr.house_number}"
        })
    df = pd.DataFrame(data)
    df.to_excel(f"{EXPORT_FOLDER}/clients.xlsx", index=False)
    df.to_json(f"{EXPORT_FOLDER}/clients.json", force_ascii=False, indent=4)
    return True

def export_all_to_json():
    all_data = {}

    def get_all_rows(model):
        return [dict(row.__data__) for row in model.select()]

    all_data["clients"] = get_all_rows(Client)
    all_data["agents"] = get_all_rows(Agent)
    all_data["real_estate"] = get_all_rows(RealEstate)
    all_data["deals"] = get_all_rows(Deal)
    all_data["contracts"] = get_all_rows(Contract)
    all_data["sales"] = get_all_rows(Sale)
    all_data["rents"] = get_all_rows(Rent)

    with open(f"{EXPORT_FOLDER}/all_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    return True
