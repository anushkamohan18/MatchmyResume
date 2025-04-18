from typing import List, Tuple, Dict
import numpy as np

# You can tweak these lists to improve categorization
TECH_KEYWORDS = ["python", "java", "c++", "django", "flask", "node", "sql", "rest", "api", "aws", "gcp", "azure"]
TOOL_KEYWORDS = ["git", "docker", "ci", "cd", "notion", "jira", "firebase", "mongodb"]
SOFT_KEYWORDS = ["communication", "team", "collaboration", "problem-solving", "leadership", "ownership"]

def compute_match_score(
    resume_keywords: List[str],
    jd_keywords: List[str]
) -> Tuple[float, List[str], Dict[str, float]]:

    resume_set = set([kw.lower() for kw in resume_keywords])
    jd_set = set([kw.lower() for kw in jd_keywords])

    matched_keywords = resume_set.intersection(jd_set)
    missing_keywords = list(jd_set - resume_set)

    match_score = round(len(matched_keywords) / max(len(jd_set), 1) * 100, 2)

    # Category-wise scoring
    category_breakdown = {
        "Technical": _category_score(matched_keywords, TECH_KEYWORDS),
        "Tools": _category_score(matched_keywords, TOOL_KEYWORDS),
        "Soft Skills": _category_score(matched_keywords, SOFT_KEYWORDS),
    }

    return match_score, missing_keywords, category_breakdown


def _category_score(matched: set, category_keywords: List[str]) -> float:
    count = sum(1 for kw in matched if kw in category_keywords)
    total = len(category_keywords)
    return round((count / total) * 100, 2) if total else 0.0
