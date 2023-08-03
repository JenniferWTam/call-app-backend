import requests
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_openai_script(user_name, party_size, reservation_time_str):
    prompt = f"Hello, {user_name} would like to make a reservation for {party_size} at {reservation_time_str}. Press one if that is available, press two if you're not available, press three if you would like some more time."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    })

    if response.status_code == 200:
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0 and "text" in data["choices"][0]:
            return data["choices"][0]["text"].strip()

    return "Failed to generate OpenAI script"
