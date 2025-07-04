import streamlit as st
from langchain_openai import ChatOpenAI
import os

local_llm = ChatOpenAI(
    model = "ai/qwen2.5:latest",
    base_url = "http://model-runner.docker.internal/engines/llama.cpp/v1",
    api_key = "nope"
)

cloud_llm = ChatOpenAI(
    model = "mistralai/mixtral-8x7b-instruct",
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.environ.get("OPENROUTER_API_KEY")
)

def write_message(role, content):
    st.session_state["messages"].append(
        {
            "role": role, 
            "content": content
        }
    )
    with st.chat_message(role):
        st.write(content)

st.title("Talk to me...")

think_harder = st.checkbox(
    "Think harder", 
    value=False
)

st.write("\n" * 10)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
if prompt := st.chat_input("Type your message here..."):
    write_message("user", prompt)

    context = ""
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            context += "User: "
        else:
            context += "Assistant: "          
        context += msg['content']
    
    # Choose model
    llm = cloud_llm if think_harder else local_llm
    response = llm.invoke(context)

    # 4️⃣ Append and render assistant message immediately
    write_message("assistant", response.content)
