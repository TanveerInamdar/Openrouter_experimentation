import streamlit as st
import pandas as pd
import numpy as np
from main import get_response
import csv
import sqlite3
import _sqlite3

st.button("Click me", width=100)

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

if prompt := st.chat_input("Enter something"):

    # Store user message
    st.session_state.query.append(
        {"role": "user", "content": prompt}
    )
    cursor.execute(insert_query,("user", prompt))
    #cursor.execute(f"""INSERT INTO messages(session_id, role, content) VALUES ("session_id1","user","{prompt}")""")
    conn.commit()
    st.chat_message("user").write(prompt)
    with st.spinner("Hold on..."):
        result = get_response(st.session_state.query)

    st.session_state.query.append(
        {"role": "assistant", "content": result}
    )

    cursor.execute(insert_query,("Assistant", result))
    #cursor.execute(f"""INSERT INTO messages(session_id, role, content) VALUES ("session_id1","assistant","{result}")""")
    conn.commit()
    st.chat_message("assistant").write(result)
