import openai
import os

def get_client():
    return openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

def get_response(prompt):
    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
