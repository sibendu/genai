import streamlit as st
import sys
sys.path.insert(1, 'autogen/research/')

from research_manager import ResearchManager

avators = {"Researcher":"https://cdn-icons-png.flaticon.com/512/320/320336.png",
            "Reporting Analyst":"https://cdn-icons-png.freepik.com/512/9408/9408201.png"}

def print_callback(recipient, messages, sender, config):
    print(sender.name + ' to ' +recipient.name + ', no of messages: '+ str(len(messages)))
    st.session_state.agent_steps.append(
        {"sender": sender.name, "recipient": recipient.name, "content": messages[-1]["content"]})

    return False, None  # required to ensure the agent communication flow continues

@st.dialog(title="Agent Steps", width="large")
def show_agent_output():
    count = 0
    #print(st.session_state.agent_steps)
    for msg in st.session_state.agent_steps:
        count = count + 1
        st.header(str(count)+ '. ' + msg["sender"] + ' to ' + msg["recipient"])
        st.write(msg["content"])
        #msg["content"]

st.title("Research")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Please enter a topic for blog you want to write"}]

if "agent_steps" not in st.session_state:
    st.session_state["agent_steps"] = []

if st.button("Agent Steps"):
    show_agent_output()

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    researchManager = ResearchManager(print_callback_function=print_callback)
    result = researchManager.run(prompt);
    result = f"## Final Result Ready"
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result)