import streamlit as st
import pandas as pd
import numpy as np
from main import get_response
import csv
import sqlite3
import _sqlite3
import os
from db_init import create_db

DB_FILE = "chat_history.db"
conn = sqlite3.connect("chat_history.db")

cursor = conn.cursor()
insert_query = f"""INSERT INTO messages(session_id, role, content) VALUES ("session_id1",?,?)"""

if "query" not in st.session_state:
    st.session_state.query = []
cursor.execute('SELECT role, content FROM messages WHERE session_id = ?', ("session_id1",))
rows = cursor.fetchall()
for row in rows:
        # row[0] is role, row[1] is content
        st.session_state.query.append({"role": row[0], "content": row[1]})

for msg in st.session_state.query:  # Initialize this for each call
    st.chat_message(msg["role"]).write(msg["content"])

if st.button("Clear current chat", width=100):
    if os.path.exists(DB_FILE):
        conn.close()
        os.remove(DB_FILE)
        create_db()
        st.session_state.query = []
        st.rerun()

if prompt := st.chat_input("Enter something"):

    # Store user message
    st.session_state.query.append(
        {"role": "user", "content": prompt}
    )
    cursor.execute(insert_query,("user", prompt))
    conn.commit()

    st.chat_message("user").write(prompt)
    with st.spinner("Hold on..."):
        result = get_response(st.session_state.query)

    st.session_state.query.append(
        {"role": "assistant", "content": result}
    )

    cursor.execute(insert_query,("Assistant", result))
    conn.commit()
    st.chat_message("assistant").write(result)
