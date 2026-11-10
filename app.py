import streamlit as st
import os

from dotenv import load_dotenv
from google import genai


# --------------------------------
# 1. LOAD API KEYS
# --------------------------------

load_dotenv()


def get_api_key(key_name):
    try:
        return st.secrets[key_name]
    except Exception:
        return os.getenv(key_name)


GEMINI_API_KEY = get_api_key("GEMINI_API_KEY")
TAVILY_API_KEY = get_api_key("TAVILY_API_KEY")


# Make API keys available to other modules
if GEMINI_API_KEY:
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

if TAVILY_API_KEY:
    os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY


# --------------------------------
# 2. INITIALIZE GEMINI
# --------------------------------

gemini_client = None

if GEMINI_API_KEY:
    gemini_client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# Import graph after loading API keys
from graph import run_research_agent


# --------------------------------
# 3. PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="AI Deep Research Agent",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------
# 4. APPLICATION TITLE
# --------------------------------

st.title("🤖 AI Deep Research Agent")

st.write(
    "Search the web and generate AI-powered research reports."
)

st.divider()


# --------------------------------
# 5. SIDEBAR
# --------------------------------

st.sidebar.title("⚙️ Settings")

st.sidebar.header("API Status")

st.sidebar.write(
    "Gemini:",
    "🟢 Connected" if gemini_client else "🔴 Not Connected"
)

st.sidebar.write(
    "Tavily:",
    "🟢 Connected" if TAVILY_API_KEY else "🔴 Not Connected"
)

st.sidebar.divider()

st.sidebar.info(
    "This application uses multiple AI agents "
    "to research and generate reports."
)


# --------------------------------
# 6. RESEARCH TOPIC INPUT
# --------------------------------

st.subheader("🔍 Research Topic")

topic = st.text_input(
    "Enter your research topic",
    placeholder="Example: Applications of Artificial Intelligence"
)


# --------------------------------
# 7. START RESEARCH
# --------------------------------

if st.button("🚀 Start Research", use_container_width=True):

    if not topic.strip():

        st.warning("Please enter a research topic.")

    elif not GEMINI_API_KEY or not TAVILY_API_KEY:

        st.error(
            "Please check your Gemini and Tavily API keys."
        )

    else:

        try:

            with st.spinner("Running AI Research Agents..."):

                result = run_research_agent(
                    topic,
                    gemini_client
                )


            st.success("Research completed successfully!")

            st.divider()


            # --------------------------------
            # RESEARCH PLAN
            # --------------------------------

            st.subheader("📋 Research Plan")

            for step in result["plan"]:

                if isinstance(step, dict):

                    st.write(
                        f"Step {step['step']}: {step['task']}"
                    )

                else:

                    st.write(step)


            st.divider()


            # --------------------------------
            # WEB SEARCH RESULTS
            # --------------------------------

            st.subheader("🌐 Web Search Results")

            for i, item in enumerate(result["research"], 1):

                with st.expander(
                    f"{i}. {item.get('title', 'Untitled Source')}"
                ):

                    st.write(item.get("content", ""))

                    url = item.get("url", "")

                    if url:
                        st.markdown(f"[Read More]({url})")


            st.divider()


            # --------------------------------
            # RESEARCH ANALYSIS
            # --------------------------------

            st.subheader("📊 Research Analysis")

            st.json(result["analysis"])


            st.divider()


            # --------------------------------
            # FACT CHECKING
            # --------------------------------

            st.subheader("✅ Fact Checking")

            st.markdown(result["fact_check"])


            st.divider()


            # --------------------------------
            # FINAL RESEARCH REPORT
            # --------------------------------

            st.subheader("📄 AI Research Report")

            st.markdown(result["report"])


            st.divider()


            # --------------------------------
            # DOWNLOAD REPORT
            # --------------------------------

            st.download_button(
                label="⬇️ Download Research Report",
                data=result["report"],
                file_name="AI_Research_Report.txt",
                mime="text/plain",
                use_container_width=True
            )


        except Exception as e:

            error_message = str(e)

            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            ):

                st.error(
                    "Gemini API daily quota exceeded. "
                    "Please try again after the quota resets."
                )

            elif (
                "503" in error_message
                or "UNAVAILABLE" in error_message
            ):

                st.warning(
                    "Gemini server is busy. Please try again later."
                )

            elif (
                "401" in error_message
                or "Unauthorized" in error_message
                or "API key not valid" in error_message
            ):

                st.error(
                    "Invalid API key. Please check your "
                    "Gemini and Tavily API keys."
                )

            else:

                st.error(
                    f"An error occurred: {error_message}"
                )


# --------------------------------
# 8. FOOTER
# --------------------------------

st.divider()

st.caption(
    "AI Deep Research Agent | Built using Python, "
    "Streamlit, Gemini API and Tavily API"
)