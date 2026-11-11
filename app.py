import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient

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
# 2. INITIALIZE CLIENTS
# --------------------------------

gemini_client = None
tavily_client = None

if GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)

if TAVILY_API_KEY:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


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
    "🟢 Key Loaded" if gemini_client else "🔴 Not Connected"
)

st.sidebar.write(
    "Tavily:",
    "🟢 Key Loaded" if tavily_client else "🔴 Not Connected"
)

st.sidebar.divider()

st.sidebar.info(
    "This application uses Gemini AI and Tavily "
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
# 7. API ERROR DISPLAY
# --------------------------------

def show_api_error(service, error):

    error_message = str(error)

    st.error(f"{service} API Error")

    if "401" in error_message or "UNAUTHENTICATED" in error_message:
        st.error(
            f"{service} API authentication failed. "
            "Please check the API key in Streamlit Secrets."
        )

    elif "403" in error_message or "PERMISSION_DENIED" in error_message:
        st.error(
            f"{service} API access denied. "
            "Please check API permissions."
        )

    elif "404" in error_message or "NOT_FOUND" in error_message:
        st.error(
            f"{service} model or endpoint not found."
        )

    elif "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
        st.warning(
            f"{service} API quota exceeded. Please try again later."
        )

    elif "503" in error_message or "UNAVAILABLE" in error_message:
        st.warning(
            f"{service} server is temporarily unavailable."
        )

    else:
        st.error(f"Error details: {error_message}")


# --------------------------------
# 8. START RESEARCH
# --------------------------------

if st.button("🚀 Start Research", use_container_width=True):

    if not topic.strip():

        st.warning("Please enter a research topic.")

    elif not GEMINI_API_KEY:

        st.error("Gemini API key is missing.")

    elif not TAVILY_API_KEY:

        st.error("Tavily API key is missing.")

    else:

        # --------------------------------
        # TEST GEMINI CONNECTION
        # --------------------------------

        try:

            with st.spinner("Testing Gemini API..."):

                gemini_test = gemini_client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents="Reply with only the word OK."
                )

            if not gemini_test or not gemini_test.text:
                raise ValueError("Gemini returned an empty response.")

            st.success("Gemini API working successfully!")

        except Exception as e:

            show_api_error("Gemini", e)
            st.stop()


        # --------------------------------
        # TEST TAVILY CONNECTION
        # --------------------------------

        try:

            with st.spinner("Testing Tavily API..."):

                tavily_test = tavily_client.search(
                    query=topic,
                    search_depth="basic",
                    max_results=1
                )

            st.success("Tavily API working successfully!")

        except Exception as e:

            show_api_error("Tavily", e)
            st.stop()


        # --------------------------------
        # RUN RESEARCH AGENT
        # --------------------------------

        try:

            with st.spinner("Running AI Research Agents..."):

                result = run_research_agent(
                    topic,
                    gemini_client
                )

            st.success("Research process completed!")

            st.divider()


            # --------------------------------
            # RESEARCH PLAN
            # --------------------------------

            st.subheader("📋 Research Plan")

            for step in result.get("plan", []):

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

            research_data = result.get("research", [])

            if research_data:

                for i, item in enumerate(research_data, 1):

                    with st.expander(
                        f"{i}. {item.get('title', 'Untitled Source')}"
                    ):

                        st.write(item.get("content", ""))

                        url = item.get("url", "")

                        if url:
                            st.markdown(f"[Read More]({url})")

            else:

                st.warning("No web search results found.")


            st.divider()


            # --------------------------------
            # RESEARCH ANALYSIS
            # --------------------------------

            st.subheader("📊 Research Analysis")

            st.json(result.get("analysis", {}))


            st.divider()


            # --------------------------------
            # FACT CHECKING
            # --------------------------------

            st.subheader("✅ Fact Checking")

            fact_check = result.get("fact_check", "")

            st.markdown(fact_check)


            st.divider()


            # --------------------------------
            # FINAL RESEARCH REPORT
            # --------------------------------

            st.subheader("📄 AI Research Report")

            report = result.get("report", "")

            st.markdown(report)


            st.divider()


            # --------------------------------
            # DOWNLOAD REPORT
            # --------------------------------

            st.download_button(
                label="⬇️ Download Research Report",
                data=report,
                file_name="AI_Research_Report.txt",
                mime="text/plain",
                use_container_width=True
            )


        except Exception as e:

            st.error("Research process failed.")

            st.exception(e)


# --------------------------------
# 9. FOOTER
# --------------------------------

st.divider()

st.caption(
    "AI Deep Research Agent | Built using Python, "
    "Streamlit, Gemini API and Tavily API"
)