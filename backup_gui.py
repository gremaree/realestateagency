import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
import threading
import datetime
import os
import json
from models import *

class BackupGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Автоматическое резервное копирование")
        self.master.geometry("400x350")

        self.backup_folder = None
        self.backup_timer = None
        self.interval = 3600  # по умолчанию 1 час

        ttk.Label(master, text="🔐 Резервное копирование", font=("Arial", 16)).pack(pady=10)

        # Выбор папки
        ttk.Button(master, text="📁 Выбрать папку для резервных копий", bootstyle="secondary", command=self.choose_backup_folder).pack(pady=10)

        # Интервал
        ttk.Label(master, text="⏱ Интервал резервного копирования:").pack()
        interval_frame = ttk.Frame(master)
        interval_frame.pack(pady=5)

        self.interval_entry = ttk.Entry(interval_frame, width=10)
        self.interval_entry.insert(0, "10")  # по умолчанию 10
        self.interval_entry.pack(side=ttk.LEFT)

        self.interval_unit_var = ttk.StringVar(value="секунды")
        ttk.Combobox(interval_frame,
                     textvariable=self.interval_unit_var,
                     values=["секунды", "минуты", "часы"],
                     state="readonly",
                     width=10).pack(side=ttk.LEFT, padx=5)

        # Кнопки управления
        btn_frame = ttk.Frame(master)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="▶ Начать", bootstyle="success", command=self.start_backup).pack(side=ttk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⏹ Остановить", bootstyle="danger", command=self.stop_backup).pack(side=ttk.LEFT, padx=5)

    def choose_backup_folder(self):
        self.backup_folder = filedialog.askdirectory()
        if self.backup_folder:
            messagebox.showinfo("Готово", f"Выбрана папка:\n{self.backup_folder}")

    def start_backup(self):
        if not self.backup_folder:
            messagebox.showerror("Ошибка", "Сначала выберите папку для сохранения")
            return

        try:
            val = int(self.interval_entry.get())
            unit = self.interval_unit_var.get()

            if unit == "секунды":
                self.interval = val
            elif unit == "минуты":
                self.interval = val * 60
            elif unit == "часы":
                self.interval = val * 60 * 60
        except:
            messagebox.showerror("Ошибка", "Введите корректный интервал")
            return

        self.schedule_backup()
        messagebox.showinfo("Успех", f"Бэкап будет происходить каждые {val} {unit}")

    def schedule_backup(self):
        self.perform_backup()
        self.backup_timer = threading.Timer(self.interval, self.schedule_backup)
        self.backup_timer.start()

    def stop_backup(self):
        if self.backup_timer:
            self.backup_timer.cancel()
            self.backup_timer = None
            messagebox.showinfo("Остановлено", "Резервное копирование остановлено")
        else:
            messagebox.showinfo("Неактивно", "Резервное копирование ещё не запущено")

    def perform_backup(self):
        if not self.backup_folder:
            return

        data = self.get_all_data()
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(self.backup_folder, f"backup_{now}.json")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_all_data(self):
        def model_to_dict_list(model):
            return [dict(obj.__data__) for obj in model.select()]

        return {
            "clients": model_to_dict_list(Client),
            "agents": model_to_dict_list(Agent),
            "real_estate": model_to_dict_list(RealEstate),
            "deals": model_to_dict_list(Deal),
            "contracts": model_to_dict_list(Contract),
            "sales": model_to_dict_list(Sale),
            "rents": model_to_dict_list(Rent),
        }

def run():
    win = ttk.Toplevel()
    BackupGUI(win)

if __name__ == '__main__':
    mysql_db.connect()
    app = ttk.Window(themename="flatly")
    BackupGUI(app)
    app.mainloop()
