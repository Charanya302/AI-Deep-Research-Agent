import time


def generate_with_retry(gemini_client, prompt, max_retries=3):

    if gemini_client is None:
        raise ValueError("Gemini client is not connected.")

    for attempt in range(max_retries):

        try:
            response = gemini_client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt
)

            if response is None:
                raise ValueError("Gemini returned an empty response.")

            if not response.text:
                raise ValueError("Gemini returned an empty response.")

            return response.text

        except Exception as e:

            error_message = str(e)

            print("Gemini API Error:", error_message)

            if "401" in error_message or "UNAUTHENTICATED" in error_message:
                raise Exception(
                    "Gemini API authentication failed. "
                    "Please check your API key."
                )

            elif "403" in error_message or "PERMISSION_DENIED" in error_message:
                raise Exception(
                    "Gemini API access denied. Check API permissions."
                )

            elif "404" in error_message or "NOT_FOUND" in error_message:
                raise Exception(
                    "Gemini model not found. Check the model name."
                )

            elif "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                raise Exception(
                    "Gemini API quota exceeded. Please try again later."
                )

            elif "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < max_retries - 1:

                    wait_time = 5 * (attempt + 1)

                    print(
                        f"Gemini server busy. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    raise Exception(
                        "Gemini server is temporarily unavailable. "
                        "Please try again later."
                    )

            else:
                raise

    raise Exception(
        "Gemini request failed after multiple attempts."
    )