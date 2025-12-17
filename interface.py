import streamlit as st
import pandas as pd
import numpy as np
from main import get_response

if "query" not in st.session_state:
    st.session_state.query = []

for msg in st.session_state.query:  # Initialize this for each call
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Enter something"):
    # Store user message
    st.session_state.query.append(
        {"role": "user", "content": prompt}
    )

    st.chat_message("user").write(prompt)
    with st.spinner("Hold on..."):
        result = get_response(st.session_state.query)

    st.session_state.query.append(
        {"role": "assistant", "content": result}
    )

    st.chat_message("assistant").write(result)
