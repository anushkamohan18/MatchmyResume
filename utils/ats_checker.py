import os
from typing import List


def run_ats_checks(resume_text: str) -> tuple:
    """
    Performs basic ATS compliance checks on the resume.
    Returns an ATS score and list of warnings if any.
    """
    warnings = []
    score = 100

    # Check length
    if len(resume_text) < 500:
        warnings.append("Resume content is too short; consider adding more detail.")
        score -= 20

    # Check for important sections
    if not any(keyword in resume_text.lower() for keyword in ["experience", "projects", "education"]):
        warnings.append("Key sections like 'Experience', 'Projects', or 'Education' are missing.")
        score -= 15

    # Contact information check
    if not any(k in resume_text.lower() for k in ["contact", "email", "phone"]):
        warnings.append("Missing contact information (email or phone).")
        score -= 10

    # Bullet point usage
    if resume_text.count("•") < 5:
        warnings.append("Consider using bullet points for readability.")
        score -= 5

    # Keyword stuffing check
    if len(set(resume_text.lower().split())) < len(resume_text.split()) * 0.5:
        warnings.append("Too many repeated words. Avoid keyword stuffing.")
        score -= 5

    # File format caution
    if not resume_text.lower().endswith("pdf"):
        warnings.append("Use PDF format to avoid parsing issues with ATS.")

    return max(score, 0), warnings