from main import get_response, new_chat
import sqlite3
import time

def backend_worker():
    insert_query = f"""INSERT INTO messages(session_id, role, content, state) VALUES (?,?,?,?)"""
    print("Worker Started.")
    conn = sqlite3.connect("chat_history.db")
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.close()


    while True:
        msg_id = None
        DB_FILE = "chat_history.db"
        conn = sqlite3.connect(DB_FILE, timeout=10)
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, session_id, content, state FROM messages WHERE state = 'Pending' LIMIT 1")
            row = cursor.fetchone()
            if row:
                msg_id = row[0]
                current_session_id = row[1]

                cursor.execute('SELECT role, content FROM messages WHERE session_id = ? ', (current_session_id,))
                rows = cursor.fetchall()
                conn.close()

                query = []
                for query_row in rows:
                    # row[0] is role, row[1] is content
                    query.append({"role": query_row[0].lower(), "content": query_row[1]})
                result = get_response(query)

                query.append(
                    {"role": "assistant", "content": result}
                )

                DB_FILE = "chat_history.db"
                conn = sqlite3.connect(DB_FILE, timeout=10)
                conn.execute("PRAGMA journal_mode=WAL;")
                cursor = conn.cursor()
                cursor.execute("UPDATE messages SET state = 'Completed' WHERE id = ?", (row[0],))
                cursor.execute(insert_query, (current_session_id, "assistant", result, "Completed"))
                conn.commit()
                conn.close()
                print(f"Worker Completed for message id {row[0]}")

                DB_FILE = "chat_history.db"
                conn = sqlite3.connect(DB_FILE, timeout=10)
                conn.execute("PRAGMA journal_mode=WAL;")
                cursor = conn.cursor()
                chat_title = cursor.execute("SELECT title from sessions WHERE session_id = ?", (current_session_id,))

                title_result = chat_title.fetchall()[0][0]
                conn.close()
                print("title changed")
                if title_result == "New Chat":
                    x = new_chat(query)
                    DB_FILE = "chat_history.db"
                    conn = sqlite3.connect(DB_FILE, timeout=10)
                    conn.execute("PRAGMA journal_mode=WAL;")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE sessions set title = ? where session_id = ?", (x, current_session_id,))
                    conn.close()
            else:
                conn.close()
                time.sleep(1)

        except Exception as e:
            print(f"ERROR: {e}")
            if 'msg_id' in locals():
                DB_FILE = "chat_history.db"
                conn = sqlite3.connect(DB_FILE, timeout=10)
                conn.execute("PRAGMA journal_mode=WAL;")
                cursor = conn.cursor()
                cursor.execute("UPDATE messages SET state = 'Failed' WHERE id = ?", (msg_id,))
                conn.commit()
                conn.close()
        # finally:
        #     conn.close()

backend_worker()
