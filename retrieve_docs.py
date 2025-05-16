from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    query: str

@app.post("/ask")
async def ask_question(q: Question):
    result = retrieve_docs(q.query)
    # Format your answer to return JSON response
    answers = [{"content": doc["content"], "source": doc["source"]} for doc in result["docs"]]
    return {"answers": answers}


# Initialize HuggingFace text generation pipeline with a small model
pipe = pipeline(
    "text2text-generation",  # <- flan uses this task type
    model="google/flan-t5-base",  # <-- lightweight model
    max_new_tokens=256
)

llm = HuggingFacePipeline(pipeline=pipe)



def self_grade(question: str, docs: list) -> dict:
    import re
    import json

    prompt = f"""
    You are an assistant grading retrieval results.
    Question: {question}
    Documents: {docs}
    
    Rate from 0 (worst) to 1 (best):
    1) Relevance - How related are these docs to the question?
    2) Coverage - How well do these docs answer the question?
    
    Reply ONLY with JSON: {{"relevance": <value>, "coverage": <value>}}
    """

    llm_response = llm(prompt)

    match = re.search(r"\{.*\}", llm_response)
    if match:
        json_response = match.group()
    else:
        json_response = '{"relevance": 0.5, "coverage": 0.5}'

    scores = json.loads(json_response)
    return scores



embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="chroma_store", embedding_function=embedding_model)

def retrieve_docs(query: str) -> dict:
    results = db.similarity_search(query)
    docs = []
    for doc in results:
        docs.append({
            "content": doc.page_content,
            "source": doc.metadata.get("source", "unknown"),
            "metadata": doc.metadata
        })
    return {"docs": docs, "query": query}

def answer_question(question: str) -> str:
    """
    Main function to retrieve docs, grade, possibly retry, and answer or fallback.
    """
    # 1. Retrieve documents
    results = retrieve_docs(question)

    # 2. Self-grade results
    scores = self_grade(question, results["docs"])

    # 3. Check if scores are too low (threshold 0.6)
    if scores["relevance"] < 0.6 or scores["coverage"] < 0.6:
        # Refine query once (simple example)
        refined_query = question + " explanation"

        # Retrieve again with refined query
        results = retrieve_docs(refined_query)

        # Self-grade refined results
        scores = self_grade(refined_query, results["docs"])

        # If still low, fallback
        if scores["relevance"] < 0.6 or scores["coverage"] < 0.6:
            return "My knowledge base does not cover that topic."

    # 4. Combine retrieved docs content into answer string
    combined_answer = " ".join([doc["content"] for doc in results["docs"]])
    sources = ", ".join([doc["source"] for doc in results["docs"]])

    # Return combined answer with sources
    return f"{combined_answer}\n\n[Sources: {sources}]"


# if __name__ == "__main__":
#     while True:
#         query = input("Enter your question: ")
#         if query.lower() in ("exit", "quit"):
#             print("Goodbye!")
#             break

#         answer = answer_question(query)
#         print("\nAnswer:\n", answer)

if __name__ == "__main__":
    while True:
        query = input("Enter your question: ")
        if query.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        answer = answer_question(query)
        print("\nAnswer:\n", answer)
