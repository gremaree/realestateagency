import tkinter as tk
from tkinter import ttk, messagebox
from models import RealEstate, Address, Apartment, House, LandPlot, mysql_db

class RealEstateGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Недвижимость")
        self.master.geometry("800x400")

        self.tree = ttk.Treeview(master, columns=("id", "Адрес", "Тип", "Площадь", "Стоимость", "Статус"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Кнопки
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Добавить", command=self.open_add_form).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete).pack(side=tk.LEFT, padx=5)

        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for re in RealEstate.select():
            addr = re.address
            address_str = f"{addr.city}, {addr.street}, {addr.house_number}"
            estate_type = self.get_type(re)
            self.tree.insert("", "end", values=(
                re.id, address_str, estate_type, re.area, re.cost, re.status
            ))

    def get_type(self, obj):
        if hasattr(obj, 'apartment'):
            return "Квартира"
        elif hasattr(obj, 'house'):
            return "Дом"
        elif hasattr(obj, 'landplot'):
            return "Участок"
        return "Неизвестно"

    def open_add_form(self):
        win = tk.Toplevel(self.master)
        win.title("Добавить недвижимость")
        win.geometry("400x500")

        labels = ["Город", "Улица", "Дом", "Площадь", "Стоимость", "Статус", "Год постройки"]
        entries = []
        for label in labels:
            tk.Label(win, text=label).pack()
            entry = tk.Entry(win)
            entry.pack()
            entries.append(entry)

        # Выбор типа объекта
        tk.Label(win, text="Тип объекта").pack()
        type_var = tk.StringVar(value="Квартира")
        types = ["Квартира", "Дом", "Участок"]
        ttk.Combobox(win, textvariable=type_var, values=types, state="readonly").pack()

        extra_fields = {}

        # Дополнительные поля в зависимости от типа
        def update_extra_fields(*args):
            for widget in extra_fields.values():
                widget[0].destroy()
                widget[1].destroy()
            extra_fields.clear()

            t = type_var.get()
            if t == "Квартира":
                lbl1 = tk.Label(win, text="Этаж")
                ent1 = tk.Entry(win)
                lbl2 = tk.Label(win, text="Комнаты")
                ent2 = tk.Entry(win)
                lbl3 = tk.Label(win, text="Номер")
                ent3 = tk.Entry(win)
                for l, e, k in zip([lbl1, lbl2, lbl3], [ent1, ent2, ent3], ["floor", "rooms", "number"]):
                    l.pack()
                    e.pack()
                    extra_fields[k] = (l, e)
            elif t == "Дом":
                lbl = tk.Label(win, text="Этажность")
                ent = tk.Entry(win)
                lbl.pack()
                ent.pack()
                extra_fields["floors"] = (lbl, ent)
            elif t == "Участок":
                lbl = tk.Label(win, text="Тип участка")
                ent = tk.Entry(win)
                lbl.pack()
                ent.pack()
                extra_fields["land_type"] = (lbl, ent)

        type_var.trace_add("write", update_extra_fields)
        update_extra_fields()

        def save():
            try:
                addr = Address.create(
                    city=entries[0].get(),
                    street=entries[1].get(),
                    house_number=entries[2].get()
                )
                obj = RealEstate.create(
                    address=addr,
                    area=float(entries[3].get()),
                    cost=float(entries[4].get()),
                    status=entries[5].get(),
                    year_built=int(entries[6].get())
                )
                t = type_var.get()
                if t == "Квартира":
                    Apartment.create(
                        real_estate=obj,
                        floor=int(extra_fields["floor"][1].get()),
                        rooms=int(extra_fields["rooms"][1].get()),
                        number=extra_fields["number"][1].get()
                    )
                elif t == "Дом":
                    House.create(
                        real_estate=obj,
                        floors=int(extra_fields["floors"][1].get())
                    )
                elif t == "Участок":
                    LandPlot.create(
                        real_estate=obj,
                        land_type=extra_fields["land_type"][1].get()
                    )
                messagebox.showinfo("Успех", "Объект добавлен!")
                win.destroy()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при добавлении: {e}")

        tk.Button(win, text="Сохранить", command=save).pack(pady=10)

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите объект для удаления.")
            return
        item = self.tree.item(selected[0])
        obj_id = item['values'][0]
        if messagebox.askyesno("Подтверждение", "Удалить объект?"):
            try:
                obj = RealEstate.get_by_id(obj_id)
                obj.delete_instance(recursive=True)
                self.refresh()
                messagebox.showinfo("Удалено", "Объект удалён.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении: {e}")

def run():
    root = tk.Toplevel()
    RealEstateGUI(root)

if __name__ == '__main__':
    mysql_db.connect()
    root = tk.Tk()
    RealEstateGUI(root)
    root.mainloop()
