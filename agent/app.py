import os
import streamlit as st
import numexpr
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage

from config import LLM_MODEL, LLM_TEMPERATURE, AGENT_MAX_ITERATIONS, SYSTEM_PROMPT

load_dotenv()

st.set_page_config(page_title="AI Agent Boilerplate", page_icon="🤖")
st.title("🤖 AI Agent Boilerplate")

with st.sidebar:
    st.header("Settings")
    openai_api_key = st.text_input(
        "OpenAI API Key", 
        type="password", 
        value=os.getenv("OPENAI_API_KEY", "")
    )
    tavily_api_key = st.text_input(
        "Tavily API Key (for web search)", 
        type="password", 
        value=os.getenv("TAVILY_API_KEY", "")
    )

@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression. Supports basic arithmetic, powers, and common math functions."""
    try:
        return str(numexpr.evaluate(expression))
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
    if tavily_api_key:
        os.environ["TAVILY_API_KEY"] = tavily_api_key
        
    llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
    
    tools = [calculator]
    if tavily_api_key:
        tools.append(TavilySearchResults(max_results=2))
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=AGENT_MAX_ITERATIONS)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if user_input := st.chat_input("Ask the agent to calculate something or search the web..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.chat_message("assistant"):
            with st.spinner("Agent is thinking and using tools..."):
                response = agent_executor.invoke({
                    "input": user_input,
                    "chat_history": st.session_state.chat_history
                })
                st.markdown(response["output"])
                
        st.session_state.messages.append({"role": "assistant", "content": response["output"]})
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        st.session_state.chat_history.append(AIMessage(content=response["output"]))
else:
    st.warning("Please enter your OpenAI API Key to begin.")
