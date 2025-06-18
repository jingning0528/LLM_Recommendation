import streamlit as st
from transformers import pipeline
from langdetect import detect
from googletrans import Translator
import openai

# === CONFIG ===
USE_OPENAI = False  # Set to True to use GPT-3.5
OPENAI_KEY = "your-openai-key"  # Replace with your key if using OpenAI

# === SETUP ===
translator = Translator()
if USE_OPENAI:
    openai.api_key = OPENAI_KEY
else:
    #qa_pipeline = pipeline("text-generation", model="tiiuae/falcon-7b-instruct", tokenizer="tiiuae/falcon-7b-instruct")
    qa_pipeline = pipeline("text-generation", model="distilgpt2")

# === Sample HR Context (simulate Dayforce policy) ===
hr_context = """
Employees have 15 vacation days per year. Dental and health insurance are included in the benefits package.
Payroll is issued bi-weekly on Friday. Remote work requires manager approval.
"""

# === STREAMLIT UI ===
st.set_page_config(page_title="HR Chatbot - English/中文", page_icon="🤖")
st.title("🤖 Multilingual HR Chatbot (English / 中文)")
st.write("Ask about your HR policies — in English or Chinese!")

user_input = st.text_input("You:", placeholder="e.g., 我的休假还有多少？ / How many vacation days do I have?")

if st.button("Ask") and user_input:
    with st.spinner("Thinking..."):
        # Detect language
        lang = detect(user_input)  # 'en' or 'zh-cn'

        # Translate input to English if needed
        if lang.startswith("zh"):
            translated_input = translator.translate(user_input, src='zh-cn', dest='en').text
        else:
            translated_input = user_input

        # Build prompt
        prompt = f"You're an HR assistant. Use this context: {hr_context}\n\nQ: {translated_input}\nA:"

        # Get model response
        if USE_OPENAI:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            answer_en = response['choices'][0]['message']['content']
        else:
            result = qa_pipeline(prompt, max_new_tokens=100)[0]['generated_text']
            answer_en = result.split("A:")[-1].strip()

        # Translate back if needed
        if lang.startswith("zh"):
            answer = translator.translate(answer_en, src='en', dest='zh-cn').text
        else:
            answer = answer_en

        st.markdown(f"**Bot:** {answer}")
