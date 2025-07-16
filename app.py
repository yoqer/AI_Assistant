from langchain_openai import ChatOpenAI
import streamlit as st
import os

# Environment Variables
OPENROUTER_API_KEY = os.environ.get(
    "OPENROUTER_API_KEY"
)

LOCAL_MODEL_NAME = os.environ.get(
    "LOCAL_MODEL_NAME"
)

REMOTE_MODEL_NAME = os.environ.get(
    "REMOTE_MODEL_NAME"
)

LOCAL_BASE_URL = os.environ.get(
    "LOCAL_BASE_URL"
)

REMOTE_BASE_URL = os.environ.get(
    "REMOTE_BASE_URL"
)

cloud_llm = ChatOpenAI(
    model = REMOTE_MODEL_NAME,
    api_key = OPENROUTER_API_KEY,
    base_url = REMOTE_BASE_URL
)

local_llm = ChatOpenAI(
    model = LOCAL_MODEL_NAME,
    api_key = "nope",
    base_url = LOCAL_BASE_URL
)

#################################

st.title("Talk to me...")

think_harder = st.checkbox(
    "Think harder...",
    value = False
)

st.session_state.setdefault(
    "messages",
    []
)

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
    
prompt = st.chat_input(
    "type you message..."
)

if prompt:
    
    st.session_state["messages"].append(
        {
            "role": "user",
            "content": prompt
        }
    )
    
    with st.chat_message("user"):
        st.write(prompt)
    
    context = ""
    
    for msg in st.session_state["messages"]:
        context += msg["role"] + ": " + msg["content"]
        
    if think_harder:
        llm = cloud_llm
    else:
        llm = local_llm

    response = llm.invoke(
        context
    )
    
    st.session_state["messages"].append(
        {
            "role": "assistant",
            "content": response.content
        }
    )

    with st.chat_message("assistant"):
        st.write(response.content)








