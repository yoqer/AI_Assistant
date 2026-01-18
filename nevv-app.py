from langchain_openai import ChatOpenAI
import streamlit as st
import os

# ==============================
# SETTINGS / ENV
# ==============================

# Local (Docker Model Runner)
LOCAL_BASE_URL = os.environ.get("LOCAL_BASE_URL", "http://model-runner.docker.internal/engines/llama.cpp/v1")
LOCAL_MODEL_NAME = os.environ.get("LOCAL_MODEL_NAME", "ai/qwen2.5")

# OpenRouter (OpenAI compatible)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# Grok (xAI) - normalmente OpenAI compatible (base URL depende de tu despliegue/proveedor)
GROK_API_KEY = os.environ.get("GROK_API_KEY", "")

# Generic remote (OpenAI compatible provider)
REMOTE_BASE_URL = os.environ.get("REMOTE_BASE_URL", "https://openrouter.ai/api/v1")
REMOTE_MODEL_NAME = os.environ.get("REMOTE_MODEL_NAME", "qwen/qwen3-30b-a3b")
REMOTE_API_KEY = os.environ.get("REMOTE_API_KEY", "")  # genérico (otro proyecto)

# "Terminator bridge" (para proveedores NO compatibles)
# En este repo no hay backend Terminator público; esto deja el hueco para integrarlo vía HTTP si lo expones.
TERMINATOR_BRIDGE_URL = os.environ.get("TERMINATOR_BRIDGE_URL", "")  # ej: http://terminator:8080/api/chat

# ==============================
# Helper: construir cliente LLM
# ==============================

def build_openai_compatible_llm(model: str, base_url: str, api_key: str) -> ChatOpenAI:
    if not api_key:
        raise ValueError("Falta API key para el proveedor remoto seleccionado.")
    return ChatOpenAI(model=model, api_key=api_key, base_url=base_url)

# ==============================
# UI
# ==============================

st.set_page_config(page_title="AI Assistant", layout="centered")

st.title("Talk to me...")

with st.sidebar:
    st.header("Proveedor / Modelo")
    st.caption("Puedes abrir el selector HTML para configurar Grok/ElevenLabs y modelos remotos.")

    st.link_button(
        "Abrir selector de modelos (HTML)",
        "/model_selector.html",
        help="Abre una página simple con pestañas para elegir proveedor, modelo y cargar imagen."
    )

    provider = st.selectbox(
        "Proveedor",
        [
            "Local (Docker Model Runner)",
            "OpenRouter (OpenAI compatible)",
            "Grok (xAI / OpenAI compatible)",
            "Custom OpenAI-compatible (otro proyecto)",
            "Terminator-Bridge (no compatible / custom)"
        ],
        index=0
    )

    if provider == "Local (Docker Model Runner)":
        st.text_input("Local base URL", value=LOCAL_BASE_URL, disabled=True)
        st.text_input("Local model", value=LOCAL_MODEL_NAME, disabled=True)

    elif provider == "OpenRouter (OpenAI compatible)":
        st.text_input("REMOTE_BASE_URL", value=REMOTE_BASE_URL, help="Normalmente https://openrouter.ai/api/v1")
        st.text_input("REMOTE_MODEL_NAME", value=REMOTE_MODEL_NAME)
        st.text_input("OPENROUTER_API_KEY", value=("***" if OPENROUTER_API_KEY else ""), type="password")

    elif provider == "Grok (xAI / OpenAI compatible)":
        st.text_input("REMOTE_BASE_URL", value=REMOTE_BASE_URL, help="Pon aquí el endpoint OpenAI-compatible de Grok/xAI si aplica")
        st.text_input("REMOTE_MODEL_NAME", value=REMOTE_MODEL_NAME, help="Ej: grok-... (depende de tu endpoint)")
        st.text_input("GROK_API_KEY", value=("***" if GROK_API_KEY else ""), type="password")

    elif provider == "Custom OpenAI-compatible (otro proyecto)":
        st.text_input("REMOTE_BASE_URL", value=REMOTE_BASE_URL, help="Tu endpoint tipo /v1")
        st.text_input("REMOTE_MODEL_NAME", value=REMOTE_MODEL_NAME)
        st.text_input("REMOTE_API_KEY", value=("***" if REMOTE_API_KEY else ""), type="password")

    else:
        st.text_input("TERMINATOR_BRIDGE_URL", value=TERMINATOR_BRIDGE_URL, help="HTTP endpoint propio que traduzca a APIs no compatibles")

    st.divider()
    st.caption("Nota: El repo TERMINATOR público no expone su selector en claro; solo hay ZIP.")
    st.link_button("Ver repo TERMINATOR", "https://github.com/yoqer/TERMINATOR")
    st.link_button("Descargar TERMINATOR_Complete.zip", "https://raw.githubusercontent.com/yoqer/TERMINATOR/main/TERMINATOR_Complete.zip")

# ==============================
# Memoria de chat
# ==============================

st.session_state.setdefault("messages", [])

# Mostrar historial
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("type your message...")

if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Construir contexto
    context = ""
    for msg in st.session_state["messages"]:
        context += msg["role"] + ": " + msg["content"] + "\n"

    # Elegir LLM
    try:
        if provider == "Local (Docker Model Runner)":
            llm = ChatOpenAI(model=LOCAL_MODEL_NAME, api_key="nope", base_url=LOCAL_BASE_URL)

        elif provider == "OpenRouter (OpenAI compatible)":
            llm = build_openai_compatible_llm(
                model=REMOTE_MODEL_NAME,
                base_url=REMOTE_BASE_URL,
                api_key=OPENROUTER_API_KEY
            )

        elif provider == "Grok (xAI / OpenAI compatible)":
            llm = build_openai_compatible_llm(
                model=REMOTE_MODEL_NAME,
                base_url=REMOTE_BASE_URL,
                api_key=GROK_API_KEY
            )

        elif provider == "Custom OpenAI-compatible (otro proyecto)":
            llm = build_openai_compatible_llm(
                model=REMOTE_MODEL_NAME,
                base_url=REMOTE_BASE_URL,
                api_key=REMOTE_API_KEY
            )

        else:
            # Placeholder: aquí iría tu integración real con TERMINATOR (HTTP/SDK)
            # En este repo no hay cliente Terminator disponible.
            raise NotImplementedError(
                "Terminator-Bridge seleccionado, pero no hay backend expuesto. "
                "Configura TERMINATOR_BRIDGE_URL y añade un cliente HTTP aquí."
            )

        response = llm.invoke(context)

        st.session_state["messages"].append({"role": "assistant", "content": response.content})
        with st.chat_message("assistant"):
            st.write(response.content)

    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"Error al invocar el modelo: {e}")
