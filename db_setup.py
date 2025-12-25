import sqlite3

# Connect to your specific database file
# based on your error message, it is 'chat_history.db'
db_name = 'chat_history.db'

try:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Enable WAL mode
    cursor.execute("PRAGMA journal_mode=WAL;")
    conn.commit()

    # Check if it worked
    cursor.execute("PRAGMA journal_mode;")
    mode = cursor.fetchone()

    print(f"Success! Database '{db_name}' journal mode is now: {mode[0]}")

except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()