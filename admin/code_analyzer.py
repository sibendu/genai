import streamlit as st
import os
import shutil
import git

from code.code_analysis import download_codebase, analyze

def download():
    st.session_state.codebase_variables["codebase"] = codebase
    code_index, code_text = download_codebase(codebase)
    st.session_state.codebase_variables["code_index"] = code_index
    st.session_state.codebase_variables["code_text"] = code_text
    st.session_state.codebase_variables["download_message"] = "### Codebase downloaded"

if "codebase_variables" not in st.session_state:
    st.session_state["codebase_variables"] = {
        "download_message": "",
        "codebase": "",
        "messages": [],
        "code_index": "",
        "code_text": "",
    }

#print(st.session_state.codebase_variables["codebase"])
codebase = st.text_input("Codebase",value= st.session_state.codebase_variables["codebase"],
                         type="default", on_change=None)
st.button("Download", on_click=download)
st.write(st.session_state.codebase_variables["download_message"])

for msg in st.session_state.codebase_variables["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.codebase_variables["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    result = analyze(prompt,
                     st.session_state.codebase_variables["code_index"],
                     st.session_state.codebase_variables["code_text"])

    st.session_state.codebase_variables["messages"].append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result)
