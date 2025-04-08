import openai
import os

def get_client():
    return openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

def get_response(prompt, language="en", summary=False):
    client = get_client()
    prompt_with_language = f"{prompt}\nLanguage: {language}\nSummary: {summary}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[{"role": "user", "content": prompt_with_language}]
    )
    return response.choices[0].message.content
