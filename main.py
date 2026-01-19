import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
import uuid
def get_response(message):
  OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": f"Bearer {OPENROUTER_API_KEY}",
      "Content-Type": "application/json",
    },
    json={
      "model": "google/gemma-3n-e2b-it:free",
      "messages" : message,
    }
  )

  response_json = response.json()
  if "choices" not in response_json:
    print("API ERROR:", response_json)
    return "ERROR"
  res = (response.json()["choices"][0]["message"]["content"])

  return res



def new_chat(message:str):
  prompt = "THis is a API call from a chat based AI app. I need you to look at the user's message and make a chat name and return ONLY the title of the chat. Dont return ANYTHING ELSE. Your job is to think of what the chat's topic is about and make a name for it. Example: if someone asks you a Calculus problem, dont put the problem as the chat name. You should say the chat name is something like: Calculus solving, Calculus Question. ALso avoid generalized names like General chat or general discussion. The aim is to have a chat title where the viewer knows what chat it was just by looking at the title."
  OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

  messages = [
    {"role": "system", "content": prompt},

    {"role": "user", "content": message},
  ]
  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": f"Bearer {OPENROUTER_API_KEY}",
      "Content-Type": "application/json",
    },
    json={
      "model": "openai/gpt-oss-20b:free",
      "messages": messages,
    }
  )

  res = (response.json()["choices"][0]["message"]["content"])
  return res
