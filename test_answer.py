from rag.retriever import retrieve_documents
from rag.answer_generator import generate_answer

# Step 1: User question
query = "What is Machine Learning?"

# Step 2: Retrieve relevant documents
documents = retrieve_documents(query, k=2)

# Step 3: Convert retrieved documents into context
context = "\n\n".join(
    doc.page_content for doc in documents
)

print("\nRetrieved Context:")
print(context)

# Step 4: Generate answer using Gemini
answer = generate_answer(query, context)

print("\nGenerated Answer:")
print(answer)