import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load Environment Variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

st.set_page_config(page_title="Groq AI Assistant", page_icon="🤖", layout="wide")
st.title("🤖 Groq AI Assistant")

if not api_key:
    st.error("GROQ_API_KEY Missing! Check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

# Sidebar Configuration
st.sidebar.header("Settings")
mode = st.sidebar.radio("Select Mode", ["Basic Chat", "RAG (Document Q&A)"])

# ----------------------------
# 1. BASIC CHAT MODE
# ----------------------------
if mode == "Basic Chat":
    st.subheader("💬 Basic Groq Chat")

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display Chat History
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    if prompt := st.chat_input("Ask something..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            api_payload = [
                {"role": "system", "content": "You are a helpful assistant."}
            ] + st.session_state.chat_messages

            response = client.chat.completions.create(
                messages=api_payload,
                model=model_name,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})

# ----------------------------
# 2. RAG CHAT MODE
# ----------------------------
elif mode == "RAG (Document Q&A)":
    st.subheader("📄 RAG Chat (Document Context)")

    doc_path = st.text_input("Document Path:", value="sample_docs/knowledge.txt")

    if os.path.exists(doc_path):
        with open(doc_path, "r", encoding="utf-8") as file:
            knowledge_text = file.read()
        
        with st.expander("View Knowledge Base Content"):
            st.text(knowledge_text)

        if "rag_messages" not in st.session_state:
            st.session_state.rag_messages = []

        for msg in st.session_state.rag_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if question := st.chat_input("Ask a question based on document..."):
            st.session_state.rag_messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                prompt_content = f"Document:\n{knowledge_text}\n\nQuestion:\n{question}"
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Answer using only the document below."},
                        {"role": "user", "content": prompt_content}
                    ],
                    model=model_name,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.rag_messages.append({"role": "assistant", "content": reply})
    else:
        st.warning(f"File not found at `{doc_path}`. Place your document file at the specified path.")