# 🤖 AI Deep Research Agent

An AI-powered research application that automates web research, collects information from multiple sources, analyzes data, performs fact-checking, and generates structured research reports using Generative AI and Retrieval-Augmented Generation (RAG).

## 📌 Project Overview

AI Deep Research Agent is a Python-based application designed to simplify the research process.

Users can enter a research topic, and the application automatically creates a research plan, searches the web using Tavily, collects relevant information, analyzes the results, and generates a detailed research report using Google Gemini.

The application also supports PDF document uploads and uses RAG to retrieve relevant information from uploaded documents through semantic search.

## 🎯 Objectives

- Automate the research process.
- Collect information from multiple web sources.
- Analyze and summarize research information.
- Verify important claims using available evidence.
- Retrieve relevant information from uploaded PDF documents.
- Generate structured AI-powered research reports.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| LangChain | LLM integration and application components |
| LangGraph | Research agent workflow |
| Google Gemini API | AI-powered analysis and report generation |
| Tavily API | Web search and information retrieval |
| ChromaDB | Vector database |
| HuggingFace Embeddings | Text embeddings |
| Sentence Transformers | Embedding model |
| PyPDF | PDF document loading |
| Python-dotenv | Environment variable management |

## ✨ Key Features

1. Automated Research Planning
2. Web Search Integration
3. Multiple-Source Information Collection
4. Research Data Analysis
5. AI-Assisted Fact Checking
6. PDF Document Upload
7. Text Splitting and Embedding Generation
8. Semantic Search using RAG
9. ChromaDB Vector Storage
10. AI-Powered Research Report Generation
11. Research Report Download

## 🏗️ Project Architecture

### Research Agent Workflow

1. **Planner Agent:** Creates a structured research plan.
2. **Researcher Agent:** Searches the web using Tavily API.
3. **Analyst Agent:** Collects and organizes research information.
4. **Fact Checker:** Checks important claims against available evidence.
5. **Report Generator:** Generates the final research report using Gemini.

### RAG Workflow

1. PDF Document Upload
2. Document Loading
3. Text Splitting
4. Embedding Generation
5. ChromaDB Vector Storage
6. Semantic Retrieval
7. Context-Based Answer Generation

## 📂 Project Structure

```text
AI-Deep-Research-Agent/
│
├── agents/
│   ├── planner.py
│   ├── researcher.py
│   ├── analyst.py
│   └── report_generator.py
│
├── rag/
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── answer_generator.py
│
├── tools/
│   └── web_search.py
│
├── utils/
│   └── helpers.py
│
├── data/
│   ├── sample.pdf
│   └── sample.txt
│
├── app.py
├── graph.py
├── requirements.txt
├── create_pdf.py
├── test_rag.py
├── test_retriever.py
├── test_answer.py
└── README.md
```

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Charanya302/AI-Deep-Research-Agent.git
```

### Step 2: Open the Project Folder

```bash
cd AI-Deep-Research-Agent
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure API Keys

Create a `.env` file in the project root directory.

Add your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Never upload your `.env` file or API keys to GitHub.

### Step 7: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🚀 How to Use

1. Open the AI Deep Research Agent application.
2. Upload a PDF document for RAG-based retrieval.
3. Enter your research topic.
4. Click the **Start Research** button.
5. Wait for the research agents to complete their workflow.
6. View the research plan and web search results.
7. Explore research analysis and retrieved PDF information.
8. Review the fact-checking results.
9. Read the generated research report.
10. Download the final report.

## 🧪 Testing

The project includes separate testing scripts:

- `test_rag.py` – Tests PDF loading, text splitting, and vector storage.
- `test_retriever.py` – Tests semantic document retrieval.
- `test_answer.py` – Tests context-based answer generation.
- `test_gemini.py` – Tests Gemini API connectivity.

## 🌐 Live Demo

Add your deployed Streamlit application link here.

## 🔮 Future Enhancements

- Support multiple PDF document uploads.
- Add DOCX and TXT document support.
- Improve research source ranking.
- Add advanced retrieval and reranking techniques.
- Generate downloadable PDF and DOCX reports.
- Improve source reliability evaluation.
- Add conversational question answering over uploaded documents.

## 👩‍💻 Developed Using

Python | Streamlit | LangChain | LangGraph | Google Gemini | Tavily | ChromaDB | RAG

---

**AI Deep Research Agent – Automating Research with Generative AI and RAG.**