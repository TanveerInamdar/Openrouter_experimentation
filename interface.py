import streamlit as st
import pandas as pd
import numpy as np
from main import get_response
import csv
import sqlite3
import _sqlite3

conn = sqlite3.connect("chat_history.db")

cursor = conn.cursor()
insert_query = f"""INSERT INTO messages(session_id, role, content) VALUES ("session_id1","user",?)"""

if "query" not in st.session_state:
    st.session_state.query = []

for msg in st.session_state.query:  # Initialize this for each call
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Enter something"):

    # Store user message
    st.session_state.query.append(
        {"role": "user", "content": prompt}
    )
    db_data = (prompt, ) # Adding second argument so that the first arg is viewed as tuple and not a container of individual alphabets as string - python behavior
    cursor.execute(insert_query, db_data)
    #cursor.execute(f"""INSERT INTO messages(session_id, role, content) VALUES ("session_id1","user","{prompt}")""")
    conn.commit()
    st.chat_message("user").write(prompt)
    with st.spinner("Hold on..."):
        result = get_response(st.session_state.query)

    st.session_state.query.append(
        {"role": "assistant", "content": result}
    )
    db_data = (result, )
    cursor.execute(insert_query, db_data)
    #cursor.execute(f"""INSERT INTO messages(session_id, role, content) VALUES ("session_id1","assistant","{result}")""")
    conn.commit()
    st.chat_message("assistant").write(result)
