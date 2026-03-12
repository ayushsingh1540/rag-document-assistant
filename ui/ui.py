import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="RAG Assistant", page_icon="🤖")

st.title("📄 Enterprise RAG Document Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Chat input
question = st.chat_input("Ask a question about your documents...")

if question:

    # Display user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    try:
        response = requests.post(
            API_URL,
            json={"question": question}
        )

        if response.status_code == 200:
            answer = response.json()["answer"]
        else:
            answer = f"API Error: {response.text}"

    except Exception as e:
        answer = f"Connection error: {e}"

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})