# main.py

# Import tools
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.schema import Document
import pandas as pd
from tools import calculator_tool
from retrieve_docs import retrieve_docs

# Tools
tools = [
    {
        "name": "calculator",
        "description": "Useful for math questions like 2+2 or 5*10",
        "function": calculator_tool,
    }
]


# Setup embeddings 
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Sample documents to store

df = pd.read_csv("data/knowledge_base.csv")

documents = []
for index, row in df.iterrows():
    documents.append(Document(
        page_content=row['content'],
        metadata={
            "source": row.get('source', 'unknown'),
            "title": row.get('title', 'No Title')
        }
    ))

# Create a Chroma DB
db = Chroma.from_documents(documents, embedding_model, persist_directory="chroma_store")

# Search it!
results = db.similarity_search("What is few-shot learning?", k=2)

# Print results
for doc in results:
    print("Found:", doc.page_content)
    print("Source:", doc.metadata.get("source", "unknown source"))

# Start a simple loop for user input
while True:
    question = input("Ask your question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break  # End the loop

    if any(op in question for op in ["+", "-", "*", "/", "**"]):
        answer = calculator_tool(question)
        print("Answer using calculator tool:", answer)
        # No 'result' here, so skip the rest of the loop
        continue

    else:
        result = retrieve_docs(question)

        printed = set()
        for doc in result["docs"]:
            key = doc["content"] + doc["source"]
            if key not in printed:
                print("Answer:", doc["content"])
                print("Source:", doc["source"])
                print("Metadata:", doc["metadata"])
                print("-" * 40)
                printed.add(key)
