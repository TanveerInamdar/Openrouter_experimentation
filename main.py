import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
def get_response(prompt: str):
  OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    },
    data=json.dumps({
      "model": "openai/gpt-oss-20b:free",
      "messages": [
        {
          "role": "user",
          "content": f"{prompt}"
        }
      ]
    })
  )
  res = (response.json()["choices"][0]["message"]["content"])
  return res


