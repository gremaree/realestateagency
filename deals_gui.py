import tkinter as tk
from tkinter import ttk, messagebox
from models import mysql_db, Deal, DealParticipant, DealRealEstate, Client, Agent, RealEstate

class DealsGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Сделки")
        self.master.geometry("800x400")

        self.tree = ttk.Treeview(master, columns=("id", "Статус", "Клиент", "Агент", "Недвижимость"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Создать сделку", command=self.open_add_form).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить сделку", command=self.delete_deal).pack(side=tk.LEFT, padx=5)

        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for deal in Deal.select():
            client_str = "-"
            agent_str = "-"
            obj_str = "-"
            participants = deal.participants
            realties = deal.real_estates

            for p in participants:
                client_str = f"{p.client.personal_data.fio.last_name} {p.client.personal_data.fio.first_name}"
                agent_str = f"{p.agent.personal_data.fio.last_name} {p.agent.personal_data.fio.first_name}"

            for r in realties:
                addr = r.real_estate.address
                obj_str = f"{addr.city}, {addr.street}, {addr.house_number}"

            self.tree.insert("", "end", values=(deal.id, deal.process_status, client_str, agent_str, obj_str))

    def open_add_form(self):
        win = tk.Toplevel(self.master)
        win.title("Создать сделку")
        win.geometry("400x400")

        # Статус сделки
        tk.Label(win, text="Статус сделки").pack()
        status_entry = tk.Entry(win)
        status_entry.pack()

        # Клиент
        tk.Label(win, text="Клиент").pack()
        client_var = tk.StringVar()
        clients = list(Client.select())
        client_map = {f"{c.id}. {c.personal_data.fio.last_name} {c.personal_data.fio.first_name}": c for c in clients}
        client_combo = ttk.Combobox(win, values=list(client_map.keys()), textvariable=client_var, state="readonly")
        client_combo.pack()

        # Агент
        tk.Label(win, text="Агент").pack()
        agent_var = tk.StringVar()
        agents = list(Agent.select())
        agent_map = {f"{a.id}. {a.personal_data.fio.last_name} {a.personal_data.fio.first_name}": a for a in agents}
        agent_combo = ttk.Combobox(win, values=list(agent_map.keys()), textvariable=agent_var, state="readonly")
        agent_combo.pack()

        # Недвижимость
        tk.Label(win, text="Объект недвижимости").pack()
        real_var = tk.StringVar()
        estates = list(RealEstate.select())
        real_map = {
            f"{r.id}. {r.address.city}, {r.address.street}, {r.address.house_number}": r
            for r in estates
        }
        real_combo = ttk.Combobox(win, values=list(real_map.keys()), textvariable=real_var, state="readonly")
        real_combo.pack()

        def save():
            try:
                deal = Deal.create(process_status=status_entry.get())
                DealParticipant.create(
                    deal=deal,
                    client=client_map[client_var.get()],
                    agent=agent_map[agent_var.get()]
                )
                DealRealEstate.create(
                    deal=deal,
                    real_estate=real_map[real_var.get()]
                )
                messagebox.showinfo("Успех", "Сделка добавлена!")
                win.destroy()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при создании сделки: {e}")

        tk.Button(win, text="Сохранить", command=save).pack(pady=10)

    def delete_deal(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите сделку для удаления.")
            return
        item = self.tree.item(selected[0])
        deal_id = item['values'][0]
        if messagebox.askyesno("Подтверждение", "Удалить сделку?"):
            try:
                deal = Deal.get_by_id(deal_id)
                deal.delete_instance(recursive=True)
                self.refresh()
                messagebox.showinfo("Удалено", "Сделка удалена.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении: {e}")

def run():
    root = tk.Toplevel()
    DealsGUI(root)

if __name__ == '__main__':
    mysql_db.connect()
    root = tk.Tk()
    DealsGUI(root)
    root.mainloop()
