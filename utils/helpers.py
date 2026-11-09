import time


def generate_with_retry(gemini_client, prompt, max_retries=3):

    for attempt in range(max_retries):

        try:
            response = gemini_client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            # Daily quota exceeded
            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                raise Exception(
                    "Gemini API daily quota exceeded. "
                    "Please wait until the quota resets."
                )

            # Temporary server overload
            elif "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)

                    print(
                        f"Gemini server busy. Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    raise Exception(
                        "Gemini server is temporarily unavailable. "
                        "Please try again later."
                    )

            else:
                raise

