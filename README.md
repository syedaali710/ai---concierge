# AI-Concierge

A local vector search API with voice capabilities that provides accurate answers from your document database.

## Features

-  **Vector Search**: Local document retrieval using ChromaDB
-  **Authentication**: Basic HTTP authentication
-  **Voice Interface**: Speech input and output capabilities
-  **FastAPI Backend**: High-performance Python web framework
-  **Intelligent Ranking**: Self-reflection algorithm for result relevance
-  **LangGraph Integration**: Efficient processing without expensive API calls

## Getting Started

### Prerequisites

- macOS
- Terminal access

### Environment Setup

1. **Install Homebrew** (if not already installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   When prompted, enter your macOS password and follow on-screen instructions.

2. **Install Python 3.12**
   ```bash
   brew install python@3.12
   python3 --version  # Verify installation
   ```

3. **Create a Virtual Environment**
   Navigate to your project folder and run:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Required Dependencies**
   ```bash
   pip install fastapi uvicorn langgraph chromadb httpbasic
   ```
   Optional packages if using voice features:
   ```bash
   pip install pyttsx3 speech_recognition
   ```

5. **Set Up Vector Store**
   Download and prepare your documents for vector search according to the LangGraph documentation.

6. **Start the API Server**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at http://127.0.0.1:8000

## Authentication

The API uses HTTP Basic Authentication with the following credentials:
- Username: `****`
- Password: `****`

## API Usage

### Testing with cURL

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -u datababe:drsamah710 \
  -H "Content-Type: application/json" \
  -d '{"query": "What is vector search?"}'
```

### Testing with HTTPie

```bash
http --auth datababe:drsamah710 POST http://127.0.0.1:8000/ask query="What is vector search?"
```

## Response Format

Successful queries return structured responses with source citations:

```json
{
  "answer": "Vector search is a technique to find similar items based on embeddings.",
  "source": "ML Basics Paper",
  "metadata": {
    "title": "Vector Search",
    "source": "ML Basics Paper"
  }
}
```

## Self-Reflection Algorithm

The system employs a sophisticated approach to ensure high-quality responses:

1. **Content Deduplication**: Prevents repeat answers by checking (content, source) tuples
2. **Score-Based Ranking**: Results are sorted by relevance score in descending order
3. **Top-K Retrieval**: Returns the top 3 non-repetitive results to balance completeness with conciseness

This methodology mimics a decay mechanism where lower-scoring results are filtered out unless they're highly relevant.

## Voice Assistant Features

The voice interface supports:

- Speech input for queries
- Text-to-speech output for responses
- Command recognition (e.g., "stop" or "exit" to end the session)

## Error Handling

The API includes robust error handling:

- Authentication failures return a 401 Unauthorized status
- Out-of-scope questions return an empty results list or low-confidence fallback
- Graceful error handling for edge cases (fewer than 3 documents, speech recognition failures)

## Registration and Login Flow

1. User makes a request to `/ask` endpoint
2. System prompts for HTTP Basic Authentication
3. If credentials match (datababe/drsamah710), the request proceeds
4. If authentication fails, a 401 Unauthorized response is returned with a header to trigger re-authentication

## Out-of-Scope Questions

When a query doesn't match documents in the vector database, the system:
- Returns an empty results list or low-confidence message
- Avoids hallucination by only retrieving existing information, not generating new content

## Contributors

Dr Samah