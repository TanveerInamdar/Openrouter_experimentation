# This will create the file 'chat_history.db' if it doesn't exist
import sqlite3
def create_db():
    conn = sqlite3.connect(f'chat_history.db')
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions
        (
        session_id TEXT PRIMARY KEY,
        title TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        
        )""")


    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(session_id)
            )
        ''')

    c.execute('''
    CREATE INDEX IF NOT EXISTS idx_session_id ON messages(session_id)
    ''')

    conn.commit()
    conn.close()
    print("done")

create_db()