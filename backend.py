from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

frontend = FastAPI()

# Sample item catalog
ITEMS = [
    {"title": "Inception", "genre": "Sci-Fi", "description": "Dream within a dream."},
    {"title": "The Godfather", "genre": "Crime", "description": "Classic mafia drama."},
    {"title": "The Matrix", "genre": "Sci-Fi", "description": "Reality-bending action."},
    {"title": "Forrest Gump", "genre": "Drama", "description": "Life is like a box of chocolates."},
]

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

@frontend.post("/recommend")
def recommend(req: ChatRequest):
    try:
        system_prompt = (
            "You are a smart recommendation assistant. Recommend 2-3 items from this list:\n\n"
            f"{ITEMS}\n\n"
            "Explain why you chose each one."
        )
        messages = [{"role": "system", "content": system_prompt}] + req.history + [{"role": "user", "content": req.message}]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )
        return {"reply": response.choices[0].message["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
