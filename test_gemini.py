import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

print("Testing Gemini API...")

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Explain Machine Learning in two sentences."
)

print("\nGemini Response:")
print(response.text)