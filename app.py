import os
import streamlit as st

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI

# RAG imports
from rag.document_loader import load_pdf_documents
from rag.text_splitter import split_documents
from rag.vector_store import create_vector_store


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
# 2. INITIALIZE GEMINI AND TAVILY
# --------------------------------

gemini_client = None
tavily_client = None

if GEMINI_API_KEY:
    gemini_client = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0
    )

if TAVILY_API_KEY:
    tavily_client = TavilyClient(
        api_key=TAVILY_API_KEY
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
    "Search the web and generate AI-powered research reports "
    "using Generative AI and RAG."
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
    "This application uses Streamlit, LangChain, "
    "Gemini API, Tavily API, LangGraph and ChromaDB."
)


# --------------------------------
# 6. PDF DOCUMENT UPLOAD
# --------------------------------

st.subheader("📄 Upload Research Documents")

uploaded_file = st.file_uploader(
    "Upload a PDF document for RAG",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success(
        f"Selected PDF: {uploaded_file.name}"
    )
else:
    st.info(
        "You can upload a PDF to include its information "
        "in the research report."
    )

st.divider()


# --------------------------------
# 7. RESEARCH TOPIC INPUT
# --------------------------------

st.subheader("🔍 Research Topic")

topic = st.text_input(
    "Enter your research topic",
    placeholder="Example: Applications of Artificial Intelligence"
)


# --------------------------------
# 8. API ERROR DISPLAY
# --------------------------------

def show_api_error(service, error):

    error_message = str(error)
    error_upper = error_message.upper()

    st.error(f"{service} API Error")

    if "401" in error_upper or "UNAUTHENTICATED" in error_upper:

        st.error(
            f"{service} API authentication failed. "
            "Please check the API key."
        )

    elif "403" in error_upper or "PERMISSION_DENIED" in error_upper:

        st.error(
            f"{service} API access denied. "
            "Please check API permissions."
        )

    elif "404" in error_upper or "NOT_FOUND" in error_upper:

        st.error(
            f"{service} model or endpoint not found."
        )

    elif "429" in error_upper or "RESOURCE_EXHAUSTED" in error_upper:

        st.warning(
            f"{service} API quota exceeded. Please try again later."
        )

    elif "503" in error_upper or "UNAVAILABLE" in error_upper:

        st.warning(
            f"{service} server is temporarily unavailable. "
            "Please try again later."
        )

    else:
        st.error(f"Error details: {error_message}")


# --------------------------------
# 9. START RESEARCH
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
        # PROCESS UPLOADED PDF
        # --------------------------------

        if uploaded_file is not None:

            try:

                with st.spinner("Processing uploaded PDF..."):

                    os.makedirs("data", exist_ok=True)

                    pdf_path = os.path.join(
                        "data",
                        "uploaded_research.pdf"
                    )

                    # Save uploaded PDF

                    with open(pdf_path, "wb") as file:

                        file.write(
                            uploaded_file.getbuffer()
                        )

                    # Load PDF

                    documents = load_pdf_documents(pdf_path)

                    st.success("PDF loaded successfully!")

                    # Split PDF into chunks

                    chunks = split_documents(documents)

                    st.success(
                        f"PDF split into {len(chunks)} text chunks!"
                    )

                    # Create vector store

                    create_vector_store(chunks)

                    st.success(
                        "PDF embeddings stored in ChromaDB successfully!"
                    )

            except Exception as e:

                st.error("PDF processing failed.")

                st.exception(e)

                st.stop()

        # --------------------------------
        # RUN RESEARCH AGENT
        # --------------------------------
        # Separate Gemini and Tavily test calls
        # have been removed to reduce unnecessary API requests.

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
                        f"Step {step.get('step', '')}: "
                        f"{step.get('task', '')}"
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

                        st.write(
                            item.get("content", "")
                        )

                        url = item.get("url", "")

                        if url:

                            st.markdown(
                                f"[Read More]({url})"
                            )

            else:

                st.warning(
                    "No web search results found."
                )

            st.divider()

            # --------------------------------
            # RESEARCH ANALYSIS
            # --------------------------------

            st.subheader("📊 Research Analysis")

            st.json(
                result.get("analysis", {})
            )

            st.divider()

            # --------------------------------
            # RAG RETRIEVED INFORMATION
            # --------------------------------

            st.subheader("📚 RAG Retrieved Information")

            rag_context = result.get("rag_context", "")

            if rag_context:

                st.success(
                    "Relevant PDF information retrieved successfully!"
                )

                st.write(rag_context)

            else:

                st.info(
                    "No relevant PDF information retrieved."
                )

            st.divider()

            # --------------------------------
            # FACT CHECKING
            # --------------------------------

            st.subheader("✅ Fact Checking")

            fact_check = result.get(
                "fact_check",
                "Fact checking unavailable."
            )

            st.markdown(fact_check)

            st.divider()

            # --------------------------------
            # FINAL RESEARCH REPORT
            # --------------------------------

            st.subheader("📄 AI Research Report")

            report = result.get(
                "report",
                ""
            ) or "No report generated."

            st.markdown(report)

            st.divider()

            # --------------------------------
            # DOWNLOAD REPORT
            # --------------------------------

            st.subheader("📥 Download Research Report")

            st.download_button(
                label="⬇️ Download Research Report",
                data=report,
                file_name="AI_Research_Report.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:

            show_api_error("Research", e)

            st.error("Research process failed.")

            st.exception(e)


# --------------------------------
# 10. FOOTER
# --------------------------------

st.divider()

st.caption(
    "AI Deep Research Agent | Built using Python, "
    "Streamlit, LangChain, LangGraph, Gemini API, "
    "Tavily API and ChromaDB"
)