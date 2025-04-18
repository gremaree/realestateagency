import tkinter as tk
from tkinter import ttk, messagebox
from models import mysql_db, Contract, Deal, Sale, Rent

class ContractsGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Договоры")
        self.master.geometry("800x400")

        self.tree = ttk.Treeview(master, columns=("id", "Сделка", "Тип", "Условия"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Добавить договор", command=self.open_add_form).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить договор", command=self.delete_contract).pack(side=tk.LEFT, padx=5)

        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for contract in Contract.select():
            deal_id = contract.deal.id
            contract_type = "—"
            terms = "—"
            if hasattr(contract, 'sale'):
                contract_type = "Продажа"
                terms = f"Дата: {contract.sale.date}"
            elif hasattr(contract, 'rent'):
                contract_type = "Аренда"
                terms = f"{contract.rent.start_date} — {contract.rent.end_date} | {contract.rent.monthly_rate} руб/мес"

            self.tree.insert("", "end", values=(contract.id, f"#{deal_id}", contract_type, terms))

    def open_add_form(self):
        win = tk.Toplevel(self.master)
        win.title("Создать договор")
        win.geometry("400x400")

        tk.Label(win, text="Сделка").pack()
        deal_var = tk.StringVar()
        deals = list(Deal.select())
        deal_map = {f"{d.id} — {d.process_status}": d for d in deals}
        deal_combo = ttk.Combobox(win, values=list(deal_map.keys()), textvariable=deal_var, state="readonly")
        deal_combo.pack()

        tk.Label(win, text="Тип договора").pack()
        type_var = tk.StringVar(value="Аренда")
        type_combo = ttk.Combobox(win, values=["Аренда", "Продажа"], textvariable=type_var, state="readonly")
        type_combo.pack()

        extra_fields = {}

        def update_fields(*args):
            for widget in extra_fields.values():
                widget[0].destroy()
                widget[1].destroy()
            extra_fields.clear()

            if type_var.get() == "Аренда":
                for label_text, key in [("Дата начала", "start"), ("Дата окончания", "end"), ("Ставка в месяц", "rate")]:
                    lbl = tk.Label(win, text=label_text)
                    ent = tk.Entry(win)
                    lbl.pack()
                    ent.pack()
                    extra_fields[key] = (lbl, ent)
            elif type_var.get() == "Продажа":
                lbl = tk.Label(win, text="Дата продажи")
                ent = tk.Entry(win)
                lbl.pack()
                ent.pack()
                extra_fields["sale_date"] = (lbl, ent)

        type_var.trace_add("write", update_fields)
        update_fields()

        def save():
            try:
                deal = deal_map[deal_var.get()]
                contract = Contract.create(deal=deal, number=f"C{deal.id:03}")
                if type_var.get() == "Аренда":
                    Rent.create(
                        contract=contract,
                        start_date=extra_fields["start"][1].get(),
                        end_date=extra_fields["end"][1].get(),
                        monthly_rate=float(extra_fields["rate"][1].get())
                    )
                else:
                    Sale.create(
                        contract=contract,
                        date=extra_fields["sale_date"][1].get()
                    )
                messagebox.showinfo("Успех", "Договор добавлен.")
                win.destroy()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при добавлении: {e}")

        tk.Button(win, text="Сохранить", command=save).pack(pady=10)

    def delete_contract(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите договор для удаления.")
            return
        item = self.tree.item(selected[0])
        contract_id = item['values'][0]
        if messagebox.askyesno("Подтверждение", "Удалить договор?"):
            try:
                contract = Contract.get_by_id(contract_id)
                contract.delete_instance(recursive=True)
                self.refresh()
                messagebox.showinfo("Удалено", "Договор удалён.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении: {e}")

def run():
    root = tk.Toplevel()
    ContractsGUI(root)

if __name__ == '__main__':
    mysql_db.connect()
    root = tk.Tk()
    ContractsGUI(root)
    root.mainloop()
