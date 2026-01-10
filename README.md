**🎉IT'S MY FIRST BIG PROJECT!!!🎉**
# 💳 Bank Application

A simple **banking application** built with **Python, Tkinter, and SQLite**,  
created as a learning project to practice software architecture, GUI design, and database management.

---

## 🚀 Features

- 👤 User registration and authentication (with bcrypt password hashing)
- 💰 Real-time balance updates
- ➕ Deposit money with input validation
- 🔐 Secure local database storage (SQLite)
- 🧩 Modular project structure for maintainability
- ⚙️ Automatic database creation and permission setup (`chmod 600` on Unix)

## ⚙️ Installation & Run

### 1️⃣ Run the application
```
python main.py
```
The GUI window will open automatically.
You can register a new user and start testing basic banking operations.
🧠 Technologies Used
  Python 3.10+
  Tkinter — graphical user interface
  SQLite3 — lightweight embedded database
  bcrypt — secure password hashing
  pathlib — file system management

🔐 Security Highlights
  Passwords are hashed using bcrypt
  Database file is created with restricted permissions (0o600)
  No hardcoded secrets or unsafe global state
  All SQL queries are parameterized (protection from SQL injection)

