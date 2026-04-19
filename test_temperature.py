# test_temperature.py
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

test_prompt = "Give me one passive income idea for someone with ₹10,000 savings."

print("=" * 60)
print("DEMONSTRATING TEMPERATURE EFFECT ON AI RESPONSES")
print("=" * 60)

for label, temp in [("🥶 Temperature = 0.1 (Conservative)", 0.1),
                     ("😊 Temperature = 0.7 (Balanced)", 0.7),
                     ("🔥 Temperature = 1.5 (Creative)", 1.5)]:
    print(f"\n{label}")
    print("-" * 40)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=test_prompt,
        config=types.GenerateContentConfig(
            temperature=temp,
            max_output_tokens=150
        )
    )
    print(response.text)