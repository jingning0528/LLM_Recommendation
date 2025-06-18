import streamlit as st
import openai
import os

# Setup
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="LLM Recommender Chatbot", page_icon="🤖", layout="wide")
st.title("🎬 LLM-Powered Conversational Recommender")

# Mock item database (could be movies, articles, etc.)
items = [
    {"title": "Inception", "genre": "Sci-Fi", "description": "Dream within a dream."},
    {"title": "The Godfather", "genre": "Crime", "description": "Classic mafia drama."},
    {"title": "The Matrix", "genre": "Sci-Fi", "description": "Reality-bending action."},
    {"title": "Forrest Gump", "genre": "Drama", "description": "Life is like a box of chocolates."},
]

# Track chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Tell me what you're interested in...")

# Chat logic
if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Build context with previous messages
    chat_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

    # System prompt to guide LLM behavior
    system_prompt = (
        "You are a smart and friendly recommendation assistant. "
        "Based on the user's input and your knowledge, recommend 2-3 items from the following list:\n\n"
        f"{items}\n\n"
        "Explain *why* each item is recommended in a conversational tone."
    )

    chat_history.insert(0, {"role": "system", "content": system_prompt})

    # Call OpenAI LLM (GPT-4 or GPT-3.5)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=chat_history,
            temperature=0.7
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"❌ Error: {e}"

    # Display LLM reply
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
