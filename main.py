import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
X = input("Say something: \n")
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
        "content": f"{X}"
      }
    ]
  })
)

print(response.json()["choices"][0]["message"]["content"])

