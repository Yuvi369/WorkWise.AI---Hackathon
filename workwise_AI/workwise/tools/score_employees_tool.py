from langchain.tools import tool
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

@tool
def score_employees(ticket_description: str, history: list) -> list:
    """
    Scores employees based on similarity of past tickets to the current one.
    Returns a list of employees with average match scores.
    """
    try:
        if not history:
            return []

        # Group history by employee
        grouped = defaultdict(list)
        for record in history:
            grouped[record["employee_name"]].append(record["ticket_summary"])

        # TF-IDF similarity setup
        all_scores = []
        for name, tickets in grouped.items():
            corpus = tickets + [ticket_description]
            vectorizer = TfidfVectorizer().fit_transform(corpus)
            vectors = vectorizer.toarray()

            sim_scores = cosine_similarity([vectors[-1]], vectors[:-1])[0]
            avg_score = (sum(sim_scores) / len(sim_scores)) * 100  # convert to percentage

            all_scores.append({
                "employee_name": name,
                "score": int(round(avg_score))  # return whole number like 75, 100
            })


        # Sort by score descending
        return sorted(all_scores, key=lambda x: x["score"], reverse=True)

    except Exception as e:
        print("❌ Error in score_employees:", e)
        return []


if __name__ == "__main__":
    desc = "Fix apex code issue in production login flow"
    hist = [
        {"employee_name": "Vasanth", "ticket_summary": "Resolved apex login failure"},
        {"employee_name": "Akash", "ticket_summary": "UI bug fix in dashboard"},
        {"employee_name": "Vasanth", "ticket_summary": "Apex trigger fix for signup"}
    ]
    print(score_employees.func(desc, hist))
