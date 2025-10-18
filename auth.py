import bcrypt
import database as db

def new_user(username: str, password: str) -> bool:
    if db.sql_command("SELECT 1 FROM users WHERE username = ?", (username,), fetch=True):
        return False
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    db.sql_command(
        "INSERT INTO users (username, password, balance, transactions) VALUES (?, ?, ?, ?)",
        (username, pw_hash, 0.0, "")
    )
    return True

def login_user(username: str, password: str) -> bool:
    row = db.sql_command("SELECT password FROM users WHERE username = ?", (username,), fetch=True)
    if not row:
        return False
    stored = row[0][0]
    if isinstance(stored, bytes):
        stored_hash = stored
    else:
        s = str(stored).strip()
        if (s.startswith("b'") and s.endswith("'")) or (s.startswith('b"') and s.endswith('"')):
            s = s[2:-1]
        stored_hash = s.encode()
    return bcrypt.checkpw(password.encode(), stored_hash)
