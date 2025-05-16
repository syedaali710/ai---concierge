# answer_evaluator.py

def grade_answer(answer_text: str, query_text: str) -> float:
    """
    Grade how well the answer matches the query.
    Simple heuristic: check if key query words appear in the answer.
    
    Returns a score from 0 (bad) to 1 (perfect).
    """
    query_words = set(query_text.lower().split())
    answer_words = set(answer_text.lower().split())

    common_words = query_words.intersection(answer_words)
    score = len(common_words) / max(len(query_words), 1)

    return score

def fallback_decision(score: float, threshold: float = 0.5) -> bool:
    """
    Decide if fallback should be triggered.
    If score below threshold, return True (fallback needed).
    """
    return score < threshold

# Example usage
if __name__ == "__main__":
    q = "What is vector search?"
    a = "Vector search finds similar documents based on vector embeddings."
    score = grade_answer(a, q)
    print(f"Score: {score}")

    fallback = fallback_decision(score)
    print(f"Fallback needed? {fallback}")
