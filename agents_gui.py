import tkinter as tk
from tkinter import ttk, messagebox
from models import Agent, PersonalData, FIO, PassportData, Address, mysql_db

class AgentsGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Агенты")
        self.master.geometry("750x400")

        self.tree = ttk.Treeview(master, columns=("id", "ФИО", "Адрес", "Паспорт", "Специализация", "Зарплата"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("ФИО", text="ФИО")
        self.tree.heading("Адрес", text="Адрес")
        self.tree.heading("Паспорт", text="Паспорт")
        self.tree.heading("Специализация", text="Специализация")
        self.tree.heading("Зарплата", text="Зарплата")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Кнопки
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Добавить агента", command=self.open_add_form).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить агента", command=self.delete_agent).pack(side=tk.LEFT, padx=5)

        self.refresh_agents()

    def refresh_agents(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for agent in Agent.select():
            fio = agent.personal_data.fio
            addr = agent.personal_data.address
            passport = agent.personal_data.passport
            self.tree.insert("", "end", values=(
                agent.id,
                f"{fio.last_name} {fio.first_name} {fio.patronymic or ''}",
                f"{addr.city}, {addr.street}, {addr.house_number}",
                f"{passport.series} {passport.number}",
                agent.specialization,
                f"{agent.salary:.2f} руб"
            ))

    def open_add_form(self):
        add_win = tk.Toplevel(self.master)
        add_win.title("Добавить агента")
        add_win.geometry("400x500")

        labels = [
            "Фамилия", "Имя", "Отчество", "Серия паспорта", "Номер паспорта",
            "Город", "Улица", "Дом", "Специализация", "Зарплата"
        ]
        entries = []

        for label in labels:
            tk.Label(add_win, text=label).pack()
            entry = tk.Entry(add_win)
            entry.pack()
            entries.append(entry)

        def save():
            try:
                fio = FIO.create(
                    last_name=entries[0].get(),
                    first_name=entries[1].get(),
                    patronymic=entries[2].get() or None
                )
                passport = PassportData.create(
                    series=entries[3].get(),
                    number=entries[4].get()
                )
                address = Address.create(
                    city=entries[5].get(),
                    street=entries[6].get(),
                    house_number=entries[7].get()
                )
                pdata = PersonalData.create(fio=fio, passport=passport, address=address)
                Agent.create(
                    personal_data=pdata,
                    specialization=entries[8].get(),
                    salary=float(entries[9].get())
                )
                messagebox.showinfo("Успех", "Агент добавлен!")
                add_win.destroy()
                self.refresh_agents()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при добавлении: {e}")

        tk.Button(add_win, text="Сохранить", command=save).pack(pady=10)

    def delete_agent(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите агента для удаления.")
            return
        item = self.tree.item(selected[0])
        agent_id = item['values'][0]
        if messagebox.askyesno("Подтверждение", "Удалить выбранного агента?"):
            try:
                agent = Agent.get_by_id(agent_id)
                agent.delete_instance(recursive=True)
                self.refresh_agents()
                messagebox.showinfo("Удалено", "Агент успешно удалён.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении: {e}")

def run():
    root = tk.Toplevel()
    AgentsGUI(root)

if __name__ == '__main__':
    mysql_db.connect()
    root = tk.Tk()
    AgentsGUI(root)
    root.mainloop()
