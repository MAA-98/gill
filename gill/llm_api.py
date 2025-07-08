import os
from openai import OpenAI

client = OpenAI()

def ask_openai(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4.1",
        input=prompt,
    )
    return response.output_text