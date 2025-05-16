Instructions for Setting Up the Environment
Use these procedures to launch the project on macOS:


> If Homebrew isn't already installed, install it.
> For macOS, Homebrew is a package manager that facilitates dependency installation. From the Homebrew website, execute the following command:
bash Copy Edit /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
> When prompted, enter your macOS password and follow the on-screen directions.
>Set up Python 3.12
>Install Python 3.12 using Homebrew:
> brew install python 3.12
> run Python 3 --version
>Establish a Virtual Environment for Python
>Run the following in the project folder:
>Python3 -m venv venv source venv/bin/activate
>Your project dependencies are isolated as a result.
>Install the necessary Python packages.
To install LangGraph, uvicorn, and FastAPI, use pip.
> Install the necessary Python packages.
Installing FastAPI, uvicorn, LangGraph, ChromaDB, and other components is done with pip:

> Installing Fastapi with pip chromadb httpbasic uvicorn langgraph
(Only install extra packages, such as pyttsx3 or speech_recognition, if necessary.)

> Create a Vector Store and LangGraph.
>download documents for vector search. To index your data locally without using API keys, see to the LangGraph documentation.
>Launch the FastAPI application.
>Launch your server using:
>The URL for the API will be http://127.0.0.1:8000.
LOCAL HOST KEY:
 username = "datababe"
 password = "drsamah710"

Self-Grading Rubric Explanation & Threshold Justification

-----FUNCTIONALITY

Core API Functions is u put in place a FastAPI server that takes in request, verifies the user, gets vector results, and provides structured responses.

Search Logic is Valid as this API uses a local database (ChromaDB) to perform true vector search, and it chooses the top three non-repeating responses based on score. This demonstrates appropriate sorting and filtering logic.

Speech input and output have been added. It understands simple commands, responds via TTS, and operates locally. 

>>> A working API that provides accurate answers, is protected by simple auth, and is enhanced by voice? That satisfies and surpasses the functional bar.

------ TOOLS 

I choosed LangGraph and ChromaDB tools because they were more eeconomical than the moree expensive OpenAI APIs. 

>>> If we use free tools, we can scale any system keeping th cost in control.

----- Error Handling
If auth fails, you will get 401. 

I tried to handle edge cases ,like  deduplication logic in place, vector search returns less than 3 documents.

When instructed to stop, the voice assistant can say "Goodbye" and fails gracefully.

>>>I tried to take real life problems

 ------ Self-reflection Algorithm Details (Including Decay Mechanism)


Self-reflection mainly refers to how the system chooses the top 3 responses to return from vector search results. I didnt implement it tradionally rather i did it by deduplication by content & source that prevents repeat answers by checking (content, source) tuples.

by using score-based sorting (decay-like effect) I rank documents by descending score. This acts like a decay , lower-scoring results get filtered unless they're in the top.

LI set the limit to 3 answers to ensure clarity, relevance, and avoid overloading the user.

----- API Testing Guide with cURL/HTTPie Examples

You can test the /ask endpoint using either curl or httpie

>>> curl -X POST "http://127.0.0.1:8000/ask" \
-u datababe:drsamah710 \
-H "Content-Type: application/json" \
-d '{"query": "What is vector search?"}'

>>> http --auth datababe:drsamah710 POST http://127.0.0.1:8000/ask query="What is vector search?"

---- --- Registration and Login Flow
I implemented a basic authentication system using HTTPBasic from FastAPI. This doesn't involve sign-up forms or databases but follows this flow

- Login Credentials: Stored in code (datababe / drsamah710).

- When user hits /ask, they're prompted for HTTP Basic Auth.

- If wrong credentials are entered:

*Returns 401 Unauthorized*

- Includes a header to trigger re-auth in the browser or client.

This can be swapped later for OAuth2 or JWT, but this method works for private/local testing and prototyping.

------Happy-Path Q&A With Citations 
user asks : "What is vector search?"
 He gets: answer": "Vector search is a technique to find similar items based on embeddings.
      "source": "ML Basics Paper",
      "metadata": 
        "title": "Vector Search",
        "source": "ML Basics Paper"

so Each result includes "source" and "metadata" so that the answer can be traced back to its origin.


---- Out-of-Scope Question Handling
If a question doesn't match anything in the vector store then the system returns an empty results list or low-confidence fallback if nothing matches. No hallucination occurs because our system doesn't generate, it only retrieves.



------Feedback Command Demonstration
In your voice assistant saying "stop" or "exit" triggers.  It provides a end to the session with a spoken message, not just a silent exit. If u successfully run it then you will know. 






