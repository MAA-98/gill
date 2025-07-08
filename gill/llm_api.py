import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(prompt: str) -> str:
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()