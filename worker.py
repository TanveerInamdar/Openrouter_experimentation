from main import get_response, new_chat
import sqlite3
import time

def backend_worker():
    insert_query = f"""INSERT INTO messages(session_id, role, content) VALUES (?,?,?)"""
    while True:
        DB_FILE = "chat_history.db"
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT id, session_id, content, state FROM messages WHERE state = 'Pending' LIMIT 1")
        row = cursor.fetchone()
        if row:
            current_session_id = row[1]

            cursor.execute('SELECT role, content FROM messages WHERE session_id = ? ', (current_session_id,))
            rows = cursor.fetchall()

            query = []
            for query_row in rows:
                # row[0] is role, row[1] is content
                query.append({"role": query_row[0], "content": query_row[1]})
            result = get_response(query)

            query.append(
                {"role": "Assistant", "content": result}
            )
            cursor.execute("UPDATE messages SET state = 'Completed' WHERE id = ?", (row[0],))
            cursor.execute(insert_query, (current_session_id, "Assistant", result))
            conn.commit()
        else:
            time.sleep(1)
        conn.close()
