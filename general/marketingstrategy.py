import streamlit as st
import sys
sys.path.insert(1, 'crewai/enterprise_content_marketing_ideas/src/')

from enterprise_content_marketing_ideas.crew import CrewaiEnterpriseContentMarketingCrew

@st.dialog(title="Agent Steps", width="large")
def show_agent_output():
    count = 0
    #print(st.session_state.agent_steps)
    for msg in st.session_state.agent_steps_marketing:
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
    st.session_state.agent_steps_marketing.append({"agent": agent_name, "thought": agentfinish.thought, "content": agentfinish.text})

def content_generator_callback(agentfinish):
    agent_name = "Content Generator"
    print(agent_name + ' finished a step')
    st.session_state.agent_steps_marketing.append({"agent": agent_name, "thought": agentfinish.thought, "content": agentfinish.text})
    #st.chat_message("assistant", avatar=avators[agent_name]).write(content)

def submit():
    st.session_state.agent_steps_marketing = []
    st.session_state["marketing_strategy_output"] = ""
    input = {"topic": topic, "company": company}
    st.session_state.marketing_strategy_input = input
    print(st.session_state.marketing_strategy_input)

    with st.spinner("Generating ..."):
        final = CrewaiEnterpriseContentMarketingCrew(
                    researcher_callback=researcher_callback,
                    content_generator_callback=content_generator_callback)\
                .crew()\
                .kickoff(inputs=input)
    st.session_state.marketing_strategy_output = final

st.title("Marketing Strategy")

if "marketing_strategy_input" not in st.session_state:
    st.session_state["marketing_strategy_input"] = {"topic": "", "company": ""}

if "marketing_strategy_output" not in st.session_state:
    st.session_state["marketing_strategy_output"] = ""

if "agent_steps_marketing" not in st.session_state:
    st.session_state["agent_steps_marketing"] = []

if st.button("Agent Steps"):
    show_agent_output()

company = st.text_input("Company", value=st.session_state.marketing_strategy_input["company"], type="default", on_change=None)
topic = st.text_input("Topic", value=st.session_state.marketing_strategy_input["topic"], type="default", on_change=None)
st.button("Submit", on_click=submit)

final = st.markdown(st.session_state.marketing_strategy_output)