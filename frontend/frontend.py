import streamlit as st
import requests

st.set_page_config(page_title="LLM Chat Recommender", page_icon="🤖")

st.title("🎬 Chat-Based LLM Recommender")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Tell me what you're interested in...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare request to FastAPI
    try:
        response = requests.post(
            "http://localhost:8000/recommend",
            json={
                "message": user_input,
                "history": st.session_state.messages[:-1]
            }
        )
        reply = response.json()["reply"]
    except Exception as e:
        reply = f"❌ Backend error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
