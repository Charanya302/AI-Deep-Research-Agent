from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):

    if not documents:
        raise ValueError("No documents available for splitting.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)

    if not chunks:
        raise ValueError("Document splitting failed.")

    return chunks