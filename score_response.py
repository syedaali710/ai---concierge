# score_response.py

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
import pandas as pd
import numpy as np

# Load documents
df = pd.read_csv("data/knowledge_base.csv")

# Split and prepare documents
documents = []
for _, row in df.iterrows():
    content = row["content"]
    metadata = {"source": row["source"]}
    documents.append(type("Doc", (), {"page_content": content, "metadata": metadata}))

# Embedder setup
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Vector DB setup
db = Chroma.from_documents(documents, embedding_model, persist_directory="chroma_store")

# Scoring Function
def score_response(query, top_k=1):
    results = db.similarity_search_with_score(query, k=top_k)
    for doc, score in results:
        print("\n🧠 Best Match:")
        print("Content:", doc.page_content)
        print("Source:", doc.metadata.get("source", "unknown"))
        print("Score (lower is better):", score)
        
        if score < 0.4:
            print("\n This is a strong match, safe to use in response.")
        else:
            print("\n Not a great match. Consider saying: 'I don't know.'")

# Test the scoring
user_question = input("Ask your question: ")
score_response(user_question)
