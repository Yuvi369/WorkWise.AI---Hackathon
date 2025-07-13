from langchain.tools import tool
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@tool
def calculate_similarity(ticket: dict, past_history: list) -> float:
    """
    Calculates a similarity score between a new ticket and an employee's past tickets.
    Higher score = more relevant experience.
    """

    try:
        if not past_history:
            return 0.0

        ticket_keywords = ticket.get("skills", []) + [ticket.get("type", "")]
        ticket_text = " ".join(ticket_keywords).lower()

        combined_docs = []
        for record in past_history:
            skills = record.get("skills_used", [])
            ttype = record.get("type", "")
            combined_docs.append(" ".join(skills + [ttype]).lower())

        # Vectorize
        vectorizer = CountVectorizer().fit([ticket_text] + combined_docs)
        vectors = vectorizer.transform([ticket_text] + combined_docs)

        similarities = cosine_similarity(vectors[0:1], vectors[1:])
        avg_score = similarities[0].mean()

        return round(avg_score, 2)

    except Exception as e:
        print("❌ Similarity calculation failed:", e)
        return 0.0

if __name__ == "__main__":
    ticket = {
        "type": "Bug",
        "skills": ["LWC", "JavaScript", "CSS"]
    }

    past_history = [
        {"type": "UI Fix", "skills_used": ["CSS", "HTML", "JavaScript"]},
        {"type": "Bug", "skills_used": ["Apex", "Salesforce"]}
    ]

    score = calculate_similarity.func(ticket, past_history)
    print("🔍 Similarity Score:", score)
