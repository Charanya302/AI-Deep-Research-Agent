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

            # Generate response using LangChain Gemini
            response = gemini_client.invoke(prompt)

            if response is None or not response.content:
                raise ValueError("Gemini returned an empty response.")

            # Convert Gemini response into normal string
            content = response.content

            if isinstance(content, str):
                answer = content

            elif isinstance(content, list):

                text_parts = []

                for item in content:

                    if isinstance(item, str):
                        text_parts.append(item)

                    elif isinstance(item, dict):

                        text = item.get("text", "")

                        if text:
                            text_parts.append(text)

                answer = "\n".join(text_parts)

            else:
                answer = str(content)

            if not answer.strip():
                raise ValueError("Gemini returned no readable text.")

            return answer.strip()

        except Exception as e:

            error_message = str(e).upper()

            print("Gemini API Error:", str(e))

            if "401" in error_message or "UNAUTHENTICATED" in error_message:
                raise Exception(
                    "Gemini API authentication failed. Check your API key."
                ) from e

            elif "403" in error_message or "PERMISSION_DENIED" in error_message:
                raise Exception(
                    "Gemini API access denied. Check API permissions."
                ) from e

            elif "404" in error_message or "NOT_FOUND" in error_message:
                raise Exception(
                    "Gemini model not found. Check the model name."
                ) from e

            elif "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                raise Exception(
                    "Gemini API quota exceeded. Please try again later."
                ) from e

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
                        "Gemini server is temporarily unavailable."
                    ) from e

            else:
                raise

    raise Exception(
        "Gemini request failed after multiple attempts."
    )