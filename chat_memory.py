# A basic in-memory message store. SAMMM REMEMBER !!!!Replace later with a real DB or LangGraph memory
from collections import defaultdict

chat_sessions = defaultdict(list)  # stores chat history keyed by username
