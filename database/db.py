import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "spendly.db"


def get_db():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create database tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "name TEXT NOT NULL,"
        "email TEXT UNIQUE NOT NULL,"
        "password_hash TEXT NOT NULL,"
        "created_at TEXT DEFAULT (datetime('now'))"
        ")"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS expenses ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "user_id INTEGER NOT NULL,"
        "amount REAL NOT NULL,"
        "category TEXT NOT NULL,"
        "date TEXT NOT NULL,"
        "description TEXT,"
        "created_at TEXT DEFAULT (datetime('now')),"
        "FOREIGN KEY (user_id) REFERENCES users(id)"
        ")"
    )

    conn.commit()
    conn.close()


def seed_db():
    """Insert sample data if not already present."""
    conn = get_db()
    cursor = conn.cursor()

    # Check if users table already has data
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Create demo user
    password_hash = generate_password_hash("demo123")
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash)
    )

    # Get the demo user's ID
    cursor.execute("SELECT id FROM users WHERE email = ?", ("demo@spendly.com",))
    user_id = cursor.fetchone()[0]

    # Insert 8 sample expenses (Food gets 2 expenses)
    expenses = [
        (150.50, "Food", "2026-04-01", "Grocery shopping"),
        (45.00, "Transport", "2026-04-03", "Uber ride to airport"),
        (2500.00, "Bills", "2026-04-05", "Electricity bill"),
        (800.00, "Health", "2026-04-07", "Doctor consultation"),
        (1200.00, "Entertainment", "2026-04-10", "Concert tickets"),
        (3500.00, "Shopping", "2026-04-12", "New shoes and clothes"),
        (500.00, "Food", "2026-04-15", "Restaurant dinner"),
        (200.00, "Other", "2026-04-18", "Miscellaneous"),
    ]

    for amount, category, date, description in expenses:
        cursor.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, category, date, description)
        )

    conn.commit()
    conn.close()


def get_user_by_email(email):
    """Fetch user by email. Returns dict-like row or None."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def create_user(name, email, password):
    """Create a new user. Returns user id or None if failed."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None
