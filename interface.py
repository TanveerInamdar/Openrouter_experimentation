import streamlit as st
from main import get_response, new_chat
import sqlite3
import _sqlite3
import os
from db_init import create_db
import uuid
import random
import time
from model_list import final_models


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
current_session_id = st.session_state.session_id

DB_FILE = "chat_history.db"

welcome_statements = ["Hey Tan, what's on your mind? ", "Hello, Tanveer", "What's up", "Greetings!", "Howdy!"]
x = random.choice(welcome_statements)
st.title(f"{x}")
#
# conn = sqlite3.connect(DB_FILE)
# cursor = conn.cursor()
# cursor.execute(f"INSERT OR IGNORE INTO sessions(session_id, title) VALUES (?, ?)", (current_session_id, "New Chat"))
# conn.commit()

insert_query = f"""INSERT INTO messages(session_id, role, content, state) VALUES (?,?,?,?)"""
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute('SELECT role, content FROM messages WHERE session_id = ? ', (current_session_id,))
rows = cursor.fetchall()
conn.close()

with st.sidebar:

    if st.button("Clear current chat", width=100):
        DB_FILE = "chat_history.db"
        conn = sqlite3.connect(DB_FILE)

        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE session_id = ?", (current_session_id,))
        cursor.execute("DELETE FROM messages where session_id = ? ", (current_session_id,))
        conn.commit()
        st.session_state.query = []
        #st.session_state.session_id = str(uuid.uuid4())
        conn.commit()
        conn.close()
        st.rerun()
    if st.button("New Chat"):
        st.session_state.session_id = str(uuid.uuid4())

        current_session_id = st.session_state.session_id
        if "query" in st.session_state:
            st.session_state.query = []
        st.rerun()

    st.divider()
    st.title("Past Chats")
    st.divider()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT title, session_id FROM sessions ORDER BY created_at DESC")
    past_chat_IDs = cursor.fetchall()
    conn.close()
    for ID in past_chat_IDs:
        chat_title = ID[0]
        unique_chat_key = ID[1]
        if st.button(label=chat_title, key=unique_chat_key):
            st.session_state.session_id = unique_chat_key
            if "query" in st.session_state:
                st.session_state.query = []
            conn.close() #Manual Close as if the code hits this block, it never reaches the script end and never terminates connection
            st.rerun()


if "query" not in st.session_state:
    st.session_state.query = []
    for row in rows:
        # row[0] is role, row[1] is content
        st.session_state.query.append({"role": row[0], "content": row[1]})

for row in rows:
    st.chat_message(row[0]).write(row[1])


if prompt := st.chat_input("Enter something"):

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(f"INSERT OR IGNORE INTO sessions(session_id, title) VALUES (?, ?)", (current_session_id, "New Chat"))
    conn.commit()
    insert_query = f"""INSERT INTO messages(session_id, role, content, state) VALUES (?,?,?,?)"""

    cursor.execute('SELECT role, content FROM messages WHERE session_id = ? ', (current_session_id,))
    rows = cursor.fetchall()
    conn.close()

    # Store user message
    st.session_state.query.append(
        {"role": "User", "content": prompt}
    )
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(insert_query,(current_session_id,"User", prompt, "Pending"))
    conn.commit()
    conn.close()

    st.chat_message("User").write(prompt)
    with st.spinner("Hold on..."):

        while True:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            curr_state = cursor.execute("SELECT state from messages WHERE session_id = ? ORDER BY id desc LIMIT 1", (current_session_id,))
            state_result = curr_state.fetchone()
            if state_result[0] == "Completed":
                conn.close()
                break
            time.sleep(0.1)
            conn.close()
        st.rerun()
model_choice = st.selectbox(
        "What model should we use?",
        final_models,
        index=None,
        placeholder="Select AI model...",

    )

st.write("You selected:", model_choice)

conn.close()
