from rag.document_loader import load_pdf_documents
from rag.text_splitter import split_documents
from rag.vector_store import create_vector_store

# Step 1: Load PDF
documents = load_pdf_documents("data/sample.pdf")
print("PDF loaded successfully!")

# Step 2: Split documents
chunks = split_documents(documents)
print("Text splitting completed!")

# Step 3: Create vector store
vector_store = create_vector_store(chunks)

print("Embeddings generated successfully!")
print("Documents stored in ChromaDB successfully!")