import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from models import User, mysql_db
from main_app_gui import MainApp

class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Вход в систему")
        self.master.geometry("300x250")

        ttk.Label(master, text="Имя пользователя:").pack(pady=5)
        self.username_entry = ttk.Entry(master)
        self.username_entry.pack()

        ttk.Label(master, text="Пароль:").pack(pady=5)
        self.password_entry = ttk.Entry(master, show='*')
        self.password_entry.pack()

        ttk.Button(master, text="Войти", bootstyle="success", command=self.login).pack(pady=10)
        ttk.Button(master, text="Регистрация", bootstyle="info", command=self.open_register_window).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            mysql_db.connect(reuse_if_open=True)
            user = User.get(User.username == username)
            if user.password == password:
                self.master.destroy()
                root = ttk.Window(themename="flatly")
                app = MainApp(root, user)
                root.mainloop()
            else:
                messagebox.showerror("Ошибка", "Неверный пароль")
        except User.DoesNotExist:
            messagebox.showerror("Ошибка", "Пользователь не найден")

    def open_register_window(self):
        win = ttk.Toplevel(self.master)
        win.title("Регистрация")
        win.geometry("300x250")

        ttk.Label(win, text="Имя пользователя").pack()
        username_entry = ttk.Entry(win)
        username_entry.pack()

        ttk.Label(win, text="Пароль").pack()
        password_entry = ttk.Entry(win, show="*")
        password_entry.pack()

        ttk.Label(win, text="Роль").pack()
        role_var = ttk.StringVar(value="agent")
        role_combo = ttk.Combobox(win, textvariable=role_var, values=["admin", "agent"], state="readonly")
        role_combo.pack()

        def register():
            if not username_entry.get() or not password_entry.get():
                messagebox.showwarning("Ошибка", "Введите имя и пароль.")
                return
            try:
                User.create(
                    username=username_entry.get(),
                    password=password_entry.get(),
                    role=role_var.get()
                )
                messagebox.showinfo("Успех", "Пользователь зарегистрирован.")
                win.destroy()
            except:
                messagebox.showerror("Ошибка", "Пользователь уже существует.")

        ttk.Button(win, text="Зарегистрироваться", bootstyle="primary", command=register).pack(pady=10)


if __name__ == '__main__':
    app = ttk.Window(themename="flatly")  # или "superhero", "cosmo", "darkly", "journal"
    LoginApp(app)
    app.mainloop()
