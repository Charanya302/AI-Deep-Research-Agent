from rag.retriever import retrieve_documents

query = "What is Machine Learning?"

results = retrieve_documents(query, k=3)

print("\nSearch Query:", query)
print("\nRetrieved Results:")

for i, doc in enumerate(results, start=1):
    print(f"\nResult {i}:")
    print(doc.page_content)