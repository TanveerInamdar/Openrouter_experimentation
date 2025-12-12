import streamlit as st
import pandas as pd
import numpy as np
from main import get_response

if prompt := st.chat_input("Enter Smth"):
    st.chat_message("user").write(prompt)
    with st.spinner("Hold on..."):
        result = get_response(str(prompt))

    st.chat_message("Assistant: ").write(result)

