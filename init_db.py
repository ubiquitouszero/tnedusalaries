import sqlite3
import os

DB_PATH = "salary_db.sqlite"
SCHEMA_PATH = "schema.sql"

def init_db():
    if not os.path.exists(SCHEMA_PATH):
        print(f"Error: {SCHEMA_PATH} not found.")
        return

    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.executescript(schema_sql)
        conn.commit()
        conn.close()
        print(f"Database {DB_PATH} initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize database: {e}")

if __name__ == "__main__":
    init_db()
