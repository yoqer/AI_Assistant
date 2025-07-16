# 🧠 Simple AI Assistant App with Chat Memory Using Docker Model Runner

This project is a **production-ready AI chat app** built with [Docker Model Runner](https://dockr.ly/4nT2saM), [Streamlit](https://streamlit.io), and [LangChain](https://python.langchain.com). It lets you talk to a local LLM running via Docker, or switch seamlessly to a large cloud-based model like those on [OpenRouter](https://openrouter.ai), all **while remembering your conversation history**.

---

## 🌟 Features

✅ Run local open-source LLMs with Docker Model Runner  
✅ Clean Streamlit chat interface with message history  
✅ Seamless switch between local and cloud models  
✅ Context-passing for memory-aware responses  
✅ Fully containerized with Docker Compose  

---

## 📸 Demo

> ![Demo Screenshot](your-screenshot.png) *(Optional - Add one!)*

---

## ⚡️ Quick Start

### 1️⃣ Prerequisites

- [Docker](https://www.docker.com) installed and updated
- Docker Model Runner **enabled** in Docker Desktop (see [official docs](https://dockr.ly/4nT2saM))

---

### 2️⃣ Clone This Repo

<pre>
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
</pre>

---

### 3️⃣ Create a `.env` File

Create a file named `.env` in the project root:

<pre>
LOCAL_BASE_URL=http://model-runner.docker.internal/engines/llama.cpp/v1
REMOTE_BASE_URL=https://openrouter.ai/api/v1
LOCAL_MODEL_NAME=ai/gemma3
REMOTE_MODEL_NAME=qwen/qwen3-30b-a3b
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
</pre>

- Replace `YOUR_OPENROUTER_API_KEY` with your actual OpenRouter key.  
- Choose any local or remote model from:
  - 👉 [Docker Model Catalog](https://dockr.ly/4eTeLQl)
  - 👉 [OpenRouter](https://openrouter.ai)

---

### 4️⃣ Run the App

<pre>
docker compose up
</pre>

Then open your browser to:

http://localhost:8501  

✅ Your AI chat app is ready to use!

---

## 🗂️ Project Structure

```
.
├── app.py                # Streamlit chat app with LangChain
├── Dockerfile            # Container for running the app
├── docker-compose.yaml   # Defines app + model services
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables (you create this)
```

---

## 🧩 How It Works

- The **llm** service in `docker-compose.yaml` uses Docker Model Runner to serve a local LLM (e.g. Gemma).
- The **ai-app** service is a Streamlit web app that:
  - Stores message history in session state
  - Passes the entire chat context to the LLM for memory-aware responses
  - Lets you switch between local and remote models with a simple checkbox

---

## 🚀 Customization

- **Change Local Model**  
  Edit `LOCAL_MODEL_NAME` and `LOCAL_BASE_URL` in your `.env`.

- **Change Remote Model**  
  Edit `REMOTE_MODEL_NAME`, `REMOTE_BASE_URL`, and your `OPENROUTER_API_KEY`.

- **Dependencies**  
  Add any extra Python packages to `requirements.txt`.

---

## 📚 Helpful Links

- 🐳 [Docker Model Runner Documentation](https://dockr.ly/4nT2saM)  
- 🔎 [Find Models in Docker Catalog](https://dockr.ly/4eTeLQl)  
- 🌐 [OpenRouter](https://openrouter.ai)  
- 🐍 [Streamlit](https://streamlit.io)  
- 🦜 [LangChain for Python](https://python.langchain.com)

---

## 🤝 Contributing

If you'd like to contribute, please create an issue and describe what you have in mind.
<br>
I'm trying to keep this repository as close as possible to the video workflow, but if you'd like to take it to the next level, I can split it in two.

---





