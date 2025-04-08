import openai
import os

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def obter_resposta(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
