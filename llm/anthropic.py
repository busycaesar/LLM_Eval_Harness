from dotenv import load_dotenv
from anthropic import Anthropic
import os

load_dotenv()

MODEL = "claude-sonnet-5"

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def infer_llm(prompt):
  response = client.messages.create(
    model=MODEL,
    max_tokens=16,
    messages=[{
      "role": "user",
      "content": prompt
    }],
  )

  return "".join(b.text for b in response.content if b.type == "text")