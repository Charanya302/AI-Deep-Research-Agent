import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(query, context):

    prompt = f"""
    You are an AI research assistant.

    Answer the question using only the given context.

    If the answer is not available in the context,
    say that the information is not available.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:
            print(f"Gemini attempt {attempt + 1} failed: {e}")

            if attempt == 2:
                raise

            time.sleep(10 * (attempt + 1))