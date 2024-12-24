import streamlit as st
import sys
sys.path.insert(1, 'latest_ai_development/src/')

from latest_ai_development.crew import LatestAiDevelopment

avators = {"Researcher":"https://cdn-icons-png.flaticon.com/512/320/320336.png",
            "Reporting Analyst":"https://cdn-icons-png.freepik.com/512/9408/9408201.png"}

@st.dialog(title="Agent Steps", width="large")
def show_agent_output():
    count = 0
    #print(st.session_state.agent_steps)
    for msg in st.session_state.agent_steps:
        count = count + 1
        st.header(str(count)+ '. ' + msg["agent"])
        st.write("Thought: "+ msg["thought"])
        msg["content"]

def researcher_callback(agentfinish):
    agent_name = "Researcher"
    print(agent_name + ' finished a step')
    #print('Thought: '+agentfinish.thought)
    #print('Output: '+agentfinish.output)
    #print('Text: '+agentfinish.text)
    st.session_state.agent_steps.append({"agent": agent_name, "thought": agentfinish.thought, "content": agentfinish.text})

def reporting_analyst_callback(agentfinish):
    agent_name = "Reporting Analyst"
    print(agent_name + ' finished a step')
    st.session_state.agent_steps.append({"agent": agent_name, "thought": agentfinish.thought, "content": agentfinish.text})
    #st.chat_message("assistant", avatar=avators[agent_name]).write(content)

st.title("Blog Writer")

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

    inputs = {
        'topic': prompt
    }

    final = LatestAiDevelopment(researcher_callback=researcher_callback,reporting_analyst_callback=reporting_analyst_callback).crew().kickoff(inputs=inputs)

    result = f"## Final Result \n\n {final}"
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result)