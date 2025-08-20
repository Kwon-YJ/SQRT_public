"""
nohup streamlit run app.py &

ps aux | grep streamlit
"""

import os
import streamlit as st

st.header("Daily Trading DashBoard")
log_dir = "../pivot/"
txt_list = os.listdir(log_dir)
txt_list = [x for x in txt_list if x.split(".")[-1] == "txt"]


st.sidebar.header("기간 선택")
file_name = st.sidebar.selectbox("select your txt files", txt_list)


st.header("output")

with open(os.path.join(log_dir, file_name)) as f:
    output = ""
    lines = f.readlines()
    for line in lines:
        output += f"{line}\n"
    st.write(output)
