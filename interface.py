import streamlit as st
import sqlite3
import uuid
import random
import time
from model_list import final_models


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
current_session_id = st.session_state.session_id

DB_FILE = "chat_history.db"
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    /* Adjust the maximum width of the main content area */
    .block-container {
        max-width: 68rem;
        padding-top: 2rem;
        padding-right: 5rem;
        padding-left: 5rem;
    }
    /* Target the container for st.chat_input */
    [data-testid="stChatInput"] {
        max-width: 58.10rem;
        margin-left: auto;
        margin-right: auto;
        left: 0;
        right: 0;
    }

    .stChatInputContainer {
        padding-left: 20px !important;
        padding-right: 20px !important;
    }
    </style>
    """,

    unsafe_allow_html=True
)
welcome_statements = ["Hey Tan, what's on your mind? ", "Hello, Tanveer", "What's up", "Greetings!", "Howdy!"]
x = random.choice(welcome_statements)

st.title(f"{x}")

insert_query = f"""INSERT INTO messages(session_id, role, content, state) VALUES (?,?,?,?)"""
with sqlite3.connect(DB_FILE) as conn:

    cursor = conn.cursor()
    cursor.execute('SELECT role, content FROM messages WHERE session_id = ? ', (current_session_id,))
    rows = cursor.fetchall()
    cursor.execute('SELECT model FROM sessions WHERE session_id = ?', (current_session_id,))
    current_model = 'openai/gpt-oss-20b:free'
    model_result = cursor.fetchone()

if model_result and model_result[0]:
    current_model = model_result[0]

with st.sidebar:

    if model_choice := st.selectbox(
            "What model should we use?",
            final_models,
            index=None,
            placeholder=f"{current_model} model",
            key=f"model_select_{current_session_id}"

    ):
        st.write("You selected:", model_choice)
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE sessions SET model = ? WHERE session_id = ?", (model_choice, current_session_id))
            print("Updated Model Choice: ", model_choice)
            conn.commit()
        current_model = model_choice
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear current chat"):
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM sessions WHERE session_id = ?", (current_session_id,))
                cursor.execute("DELETE FROM messages where session_id = ? ", (current_session_id,))
                conn.commit()
                #st.session_state.session_id = str(uuid.uuid4())
                conn.commit()
            st.rerun()
    with col2:
        if st.button("New Chat"):
            st.session_state.session_id = str(uuid.uuid4())
            current_session_id = st.session_state.session_id
            st.rerun(scope="app")

    st.divider()
    st.title("Past Chats")
    st.divider()

    with sqlite3.connect(DB_FILE) as conn:

        cursor = conn.cursor()
        cursor.execute("SELECT title, session_id FROM sessions ORDER BY created_at DESC")
        past_chat_IDs = cursor.fetchall()
    for ID in past_chat_IDs:
        chat_title = ID[0]
        unique_chat_key = ID[1]
        if st.button(label=chat_title, key=unique_chat_key):
            st.session_state.session_id = unique_chat_key
            st.rerun()

for row in rows:
    st.chat_message(row[0]).write(row[1])

with sqlite3.connect(DB_FILE) as conn:

    cursor = conn.cursor()
    curr_state = cursor.execute("SELECT state from messages WHERE session_id = ? ORDER BY id desc LIMIT 1",
                            (current_session_id,))
    latest_message_status = curr_state.fetchone()

if latest_message_status and latest_message_status[0] == 'Pending':
    print("Pending API call detected. Started Pending answer workflow")
    with st.spinner("Hold on..."):

        while True:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                curr_state = cursor.execute("SELECT state from messages WHERE session_id = ? ORDER BY id desc LIMIT 1",
                                            (current_session_id,))
                latest_message_status = curr_state.fetchone()
                if latest_message_status[0] != "Pending":
                    break
                time.sleep(0.1)
        st.rerun()

provider, slash, cleaned_model_name = current_model.partition("/")
if prompt := st.chat_input(f"Talking to {cleaned_model_name}"):

    with sqlite3.connect(DB_FILE) as conn:

        cursor = conn.cursor()

        cursor.execute(f"INSERT OR IGNORE INTO sessions(session_id, title) VALUES (?, ?)", (current_session_id, "New Chat"))
        cursor.execute("UPDATE sessions SET model = ? WHERE session_id = ?", (current_model, current_session_id))
        print("Updated AI Model: ", current_model)
        conn.commit()

        insert_query = f"""INSERT INTO messages(session_id, role, content, state) VALUES (?,?,?,?)"""

        cursor.execute('SELECT role, content FROM messages WHERE session_id = ? ', (current_session_id,))
        rows = cursor.fetchall()

        cursor.execute(insert_query,(current_session_id,"User", prompt, "Pending"))
        conn.commit()

    st.chat_message("User").write(prompt)
    with st.spinner("Hold on..."):

        while True:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                curr_state = cursor.execute("SELECT state from messages WHERE session_id = ? ORDER BY id desc LIMIT 1", (current_session_id,))
                state_result = curr_state.fetchone()
            if state_result[0] == "Completed":
                break
            time.sleep(0.1)
        st.rerun()



