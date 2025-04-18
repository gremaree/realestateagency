import pandas as pd
from models import Agent, DealParticipant
from models import Rent, Sale
from datetime import datetime

def top_agents_report(limit=5):
    stats = {}

    for dp in DealParticipant.select():
        agent = dp.agent
        key = f"{agent.personal_data.fio.last_name} {agent.personal_data.fio.first_name}"
        stats[key] = stats.get(key, 0) + 1

    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)[:limit]

    df = pd.DataFrame(sorted_stats, columns=["Агент", "Кол-во сделок"])
    df.to_excel("exports/top_agents.xlsx", index=False)
    return df

def monthly_revenue_report():
    rent_data = {}
    sale_data = {}

    for r in Rent.select():
        month = r.start_date.strftime("%Y-%m")
        rent_data[month] = rent_data.get(month, 0) + float(r.monthly_rate)

    for s in Sale.select():
        month = s.date.strftime("%Y-%m")
        sale_data[month] = sale_data.get(month, 0) + 1  # можно заменить на сумму продаж, если добавить поле стоимости

    all_months = sorted(set(rent_data.keys()) | set(sale_data.keys()))

    rows = []
    for m in all_months:
        rows.append({
            "Месяц": m,
            "Аренда (₽)": rent_data.get(m, 0),
            "Продажа (шт)": sale_data.get(m, 0)
        })

    df = pd.DataFrame(rows)
    df.to_excel("exports/monthly_revenue.xlsx", index=False)
    return df