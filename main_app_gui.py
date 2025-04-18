import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from models import User, mysql_db
from export_utils import export_clients, export_all_to_json
from reports_utils import top_agents_report, monthly_revenue_report

class MainApp:
    def __init__(self, master, user):
        self.master = master
        self.master.title("Агентство недвижимости — Главное меню")
        self.master.geometry("400x500")
        self.user = user

        ttk.Label(master, text=f"Добро пожаловать, {user.username}!", font=("Arial", 14)).pack(pady=10)
        ttk.Label(master, text=f"Роль: {user.role}", font=("Arial", 10)).pack(pady=5)

        if user.role == 'admin':
            self.add_button("👥 Клиенты", self.open_clients, "primary")
            self.add_button("🧑‍💼 Агенты", self.open_agents, "primary")

        self.add_button("🏘 Недвижимость", self.open_realestate, "secondary")
        self.add_button("🤝 Сделки", self.open_deals, "secondary")

        if user.role == 'admin':
            self.add_button("📄 Договоры", self.open_contracts, "secondary")
            self.add_button("📤 Экспорт данных", self.export_data, "info")
            self.add_button("📈 Отчёт: Топ агентов", self.show_top_agents, "warning")
            self.add_button("📊 Отчёт: Аренда/Продажи", self.show_monthly_revenue, "warning")

        self.add_button("🚪 Выход", master.quit, "danger")

    def add_button(self, text, command, style):
        ttk.Button(self.master, text=text, width=30, bootstyle=style, command=command).pack(pady=5)

    def open_clients(self):
        from clients_gui import ClientsGUI
        top = ttk.Toplevel(self.master)
        ClientsGUI(top)

    def open_agents(self):
        from agents_gui import AgentsGUI
        top = ttk.Toplevel(self.master)
        AgentsGUI(top)

    def open_realestate(self):
        from realestate_gui import RealEstateGUI
        top = ttk.Toplevel(self.master)
        RealEstateGUI(top)

    def open_deals(self):
        from deals_gui import DealsGUI
        top = ttk.Toplevel(self.master)
        DealsGUI(top)

    def open_contracts(self):
        from contracts_gui import ContractsGUI
        top = ttk.Toplevel(self.master)
        ContractsGUI(top)

    def export_data(self):
        import os
        if not os.path.exists("exports"):
            os.makedirs("exports")
        try:
            export_clients()
            export_all_to_json()
            messagebox.showinfo("Успех", "Файлы экспортированы в папку 'exports'.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте: {e}")

    def show_top_agents(self):
        try:
            df = top_agents_report()
            win = ttk.Toplevel(self.master)
            win.title("Топ агентов")
            tree = ttk.Treeview(win, columns=list(df.columns), show="headings")
            for col in df.columns:
                tree.heading(col, text=col)
            for _, row in df.iterrows():
                tree.insert("", "end", values=list(row))
            tree.pack(fill="both", expand=True)
            ttk.Label(win, text="Отчёт также сохранён в exports/top_agents.xlsx").pack(pady=5)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка в отчёте: {e}")

    def show_monthly_revenue(self):
        try:
            df = monthly_revenue_report()
            win = ttk.Toplevel(self.master)
            win.title("Отчёт: Доход по месяцам")
            tree = ttk.Treeview(win, columns=list(df.columns), show="headings")
            for col in df.columns:
                tree.heading(col, text=col)
            for _, row in df.iterrows():
                tree.insert("", "end", values=list(row))
            tree.pack(fill="both", expand=True)
            ttk.Label(win, text="Отчёт также сохранён в exports/monthly_revenue.xlsx").pack(pady=5)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка в отчёте: {e}")


if __name__ == '__main__':
    mysql_db.connect()
    user = User.get(User.username == "admin1")  # Замените на нужного пользователя
    app = ttk.Window(themename="superhero")  # Можно: flatly, minty, cosmo, journal, darkly, etc.
    MainApp(app, user)
    app.mainloop()
