import tkinter as tk
from tkinter import ttk, messagebox
from models import Client, PersonalData, FIO, PassportData, Address, mysql_db

class ClientsGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Клиенты")
        self.master.geometry("700x400")

        self.tree = ttk.Treeview(master, columns=("id", "ФИО", "Адрес", "Паспорт"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("ФИО", text="ФИО")
        self.tree.heading("Адрес", text="Адрес")
        self.tree.heading("Паспорт", text="Паспорт")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Кнопки
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Добавить клиента", command=self.open_add_form).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить клиента", command=self.delete_client).pack(side=tk.LEFT, padx=5)

        self.refresh_clients()

    def refresh_clients(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for client in Client.select():
            fio = client.personal_data.fio
            addr = client.personal_data.address
            passport = client.personal_data.passport
            self.tree.insert("", "end", values=(
                client.id,
                f"{fio.last_name} {fio.first_name} {fio.patronymic or ''}",
                f"{addr.city}, {addr.street}, {addr.house_number}",
                f"{passport.series} {passport.number}"
            ))

    def open_add_form(self):
        add_win = tk.Toplevel(self.master)
        add_win.title("Добавить клиента")
        add_win.geometry("400x400")

        labels = [
            "Фамилия", "Имя", "Отчество", "Серия паспорта", "Номер паспорта",
            "Город", "Улица", "Дом"
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
                Client.create(personal_data=pdata)
                messagebox.showinfo("Успех", "Клиент добавлен!")
                add_win.destroy()
                self.refresh_clients()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при добавлении: {e}")

        tk.Button(add_win, text="Сохранить", command=save).pack(pady=10)

    def delete_client(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите клиента для удаления.")
            return
        item = self.tree.item(selected[0])
        client_id = item['values'][0]
        if messagebox.askyesno("Подтверждение", "Удалить выбранного клиента?"):
            try:
                client = Client.get_by_id(client_id)
                client.delete_instance(recursive=True)
                self.refresh_clients()
                messagebox.showinfo("Удалено", "Клиент успешно удалён.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении: {e}")

def run():
    root = tk.Toplevel()
    ClientsGUI(root)

if __name__ == '__main__':
    mysql_db.connect()
    root = tk.Tk()
    ClientsGUI(root)
    root.mainloop()
