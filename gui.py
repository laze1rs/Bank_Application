import tkinter as tk
from auth import new_user, login_user
from tkinter import messagebox
import database as db

CURRENT_USER = None

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bank Application")
        self.geometry("400x300")
        self.balance_var = tk.StringVar()
        self.current_user = None

        self.show_balance()
        self.start_register()
        self.start_login()

    def show_balance(self):
        # создаём метку, привязанную к StringVar, и запускаем периодическое обновление
        balance_label = tk.Label(self, textvariable=self.balance_var)
        balance_label.pack(pady=20)

        add_money_button = tk.Button(self, text="Add Money", command=self.add_money)
        add_money_button.pack(pady=10)

        # первое обновление и затем каждое 3000 мс
        self.update_balance()

    def update_balance(self):
        # если пользователь не залогинен — показываем сообщение
        if not self.current_user:
            self.balance_var.set("Not logged in")
            self.after(3000, self.update_balance)
            return

        # получаем актуальный баланс из БД для текущего пользователя
        res = db.sql_command("SELECT balance FROM users WHERE username = ?", (self.current_user,), fetch=True)
        if res and len(res) > 0 and res[0][0] is not None:
            bal = res[0][0]
        else:
            bal = 0.0
        self.balance_var.set(f"Current Balance: ${bal:.2f}")
        # планируем следующий вызов через 3000 мс
        self.after(3000, self.update_balance)

    def add_money(self):
        add_window = tk.Toplevel(self)
        amout_label = tk.Label(add_window, text="Enter Sum to Add:")
        amout_label.pack(pady=10)
        amout_entry = tk.Entry(add_window)
        amout_entry.pack(pady=5)
        confirm_button = tk.Button(add_window, text="Confirm", command=lambda: self.confirm_add(amout_entry.get(), add_window))
        confirm_button.pack(pady=10)

    def confirm_add(self, amount, window):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive.")
            if not self.current_user:
                raise ValueError("No user logged in.")
            db.sql_command("UPDATE users SET balance = balance + ? WHERE username = ?", (amount, self.current_user))
            window.destroy()
            # обновить отображение сразу после изменения
            self.update_balance()
        except ValueError as e:
            error_label = tk.Label(window, text=str(e), fg="red")
            error_label.pack()       
       
    def open_login(self):
        login_win = tk.Toplevel(self)
        login_win.title("Login User")

        user_label = tk.Label(login_win, text="Username:")
        user_label.pack(pady=5)
        user_entry = tk.Entry(login_win)
        user_entry.pack(pady=5)

        pass_label = tk.Label(login_win, text="Password:")
        pass_label.pack(pady=5)
        pass_entry = tk.Entry(login_win, show="*")
        pass_entry.pack(pady=5)

        login_button = tk.Button(login_win, text="Login", command=lambda: self.login(user_entry.get(), pass_entry.get(), login_win))
        login_button.pack(pady=10)
    
    def open_register(self):
        reg_win = tk.Toplevel(self)
        reg_win.title("Register User")

        user_label = tk.Label(reg_win, text="Username:")
        user_label.pack(pady=5)
        user_entry = tk.Entry(reg_win)
        user_entry.pack(pady=5)

        pass_label = tk.Label(reg_win, text="Password:")
        pass_label.pack(pady=5)
        pass_entry = tk.Entry(reg_win, show="*")
        pass_entry.pack(pady=5)

        reg_button = tk.Button(reg_win, text="Register", command=lambda: self.register(user_entry.get(), pass_entry.get(), reg_win))
        reg_button.pack(pady=10)

    def register(self, username, password, window=None):
        if not username or not password:
            messagebox.showerror("Error", "Username and password required.")
            return
        try:
            password = tk.StringVar(value=password).get()
            username = tk.StringVar(value=username).get()
            created = new_user(username, password)
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
            return

        if created:
            # set current user on successful registration
            global CURRENT_USER
            CURRENT_USER = username
            self.current_user = username
            messagebox.showinfo("Success", "User registered successfully.")
            if window:
                window.destroy()
            # обновить отображение сразу после изменения
            self.update_balance()
        else:
            messagebox.showerror("Error", "Username already exists.")

    def login(self, username, password, window=None):
        try:
            ok = login_user(username, password)
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {e}")
            return

        if ok:
            global CURRENT_USER
            CURRENT_USER = username
            self.current_user = username
            messagebox.showinfo("Success", "Logged in.")
            if window:
                window.destroy()
            self.update_balance()
        else:
            messagebox.showerror("Error", "Invalid credentials.")
    
    def start_login(self):
        login_button = tk.Button(self, text="Login User", command=self.open_login)
        login_button.pack(pady=10)

    def start_register(self):
        register_button = tk.Button(self, text="Register User", command=self.open_register)
        register_button.pack(pady=10)


app = MainWindow()
app.mainloop()
