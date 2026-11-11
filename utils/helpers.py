import time


def generate_with_retry(gemini_client, prompt, max_retries=3):

    # Validate Gemini client
    if gemini_client is None:
        raise ValueError("Gemini client is not connected.")

    # Validate prompt
    if not prompt or not prompt.strip():
        raise ValueError("Research prompt cannot be empty.")

    # Validate retry count
    if max_retries < 1:
        raise ValueError("Maximum retries must be at least 1.")

    for attempt in range(max_retries):

        try:

            response = gemini_client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            if response is None or not response.text:
                raise ValueError("Gemini returned an empty response.")

            return response.text

        except Exception as e:

            error_message = str(e).upper()

            print("Gemini API Error:", str(e))

            # Authentication error
            if "401" in error_message or "UNAUTHENTICATED" in error_message:
                raise Exception(
                    "Gemini API authentication failed. "
                    "Please check your API key."
                ) from e

            # Permission error
            elif "403" in error_message or "PERMISSION_DENIED" in error_message:
                raise Exception(
                    "Gemini API access denied. Check API permissions."
                ) from e

            # Model error
            elif "404" in error_message or "NOT_FOUND" in error_message:
                raise Exception(
                    "Gemini model not found. Check the model name."
                ) from e

            # Quota error
            elif "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                raise Exception(
                    "Gemini API quota exceeded. Please try again later."
                ) from e

            # Temporary server error
            elif (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "500" in error_message
            ):

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
                    ) from e

            else:
                raise

    raise Exception(
        "Gemini request failed after multiple attempts."
    )