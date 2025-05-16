# app.py

# 1. Importing FastAPI and required stuff 
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from retrieve_docs import retrieve_docs

# Chat memory
from typing import List
from collections import defaultdict

# 2. Create FastAPI app
app = FastAPI()

# 3. Setting up basic auth
security = HTTPBasic()

# In-memory chat history (for demo only)
chat_memory = defaultdict(list)

# 4. Authentication function
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Authenticate the user with hardcoded username/password.
    You can later replace this with real auth.
    """
    correct_username = "admin"
    correct_password = "secret"

    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

#5. Defining input request schema
class QueryRequest(BaseModel):
    query: str

# 6. /ask endpoint
@app.post("/ask")
async def ask_endpoint(query: QueryRequest, username: str = Depends(authenticate)):
    """
    Accepts a JSON query, retrieves vector search results, and returns formatted answers.
    Auth required.
    """
    question = query.query
    result = retrieve_docs(question)

    docs = result.get("docs", [])
    docs_sorted = sorted(docs, key=lambda x: x.get("score", 0), reverse=True)

    seen = set()
    top_docs = []
    for doc in docs_sorted:
        key = (doc.get("content", ""), doc.get("source", "unknown"))
        if key not in seen:
            top_docs.append(doc)
            seen.add(key)
        if len(top_docs) == 3:
            break

    response = []
    for doc in top_docs:
        response.append({
            "answer": doc.get("content", ""),
            "source": doc.get("source", "unknown"),
            "metadata": doc.get("metadata", {})
        })

    return {"results": response}

# 7. /chat endpoint
@app.post("/chat")
async def chat_endpoint(query: QueryRequest, username: str = Depends(authenticate)):
    """
    Chat endpoint that remembers previous messages per user session.
    It retrieves related context with memory and appends history.
    """
    question = query.query

    # Combining memory and current question ding ding ding
    history = chat_memory[username]
    combined_context = " ".join([msg for msg in history]) + " " + question

    result = retrieve_docs(combined_context)
    docs = result.get("docs", [])
    docs_sorted = sorted(docs, key=lambda x: x.get("score", 0), reverse=True)

    seen = set()
    top_docs = []
    for doc in docs_sorted:
        key = (doc.get("content", ""), doc.get("source", "unknown"))
        if key not in seen:
            top_docs.append(doc)
            seen.add(key)
        if len(top_docs) == 3:
            break

    response = []
    for doc in top_docs:
        response.append({
            "answer": doc.get("content", ""),
            "source": doc.get("source", "unknown"),
            "metadata": doc.get("metadata", {})
        })

    # Add current question to history
    chat_memory[username].append(question)
    if len(chat_memory[username]) > 10:
        chat_memory[username] = chat_memory[username][-10:]  # keepingg last 10

    return {"results": response}

#tadaaa!!