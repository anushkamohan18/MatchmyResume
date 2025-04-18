import re

def clean_job_description(jd_text: str) -> str:
    """
    Cleans up the pasted job description by:
    - Lowercasing
    - Removing special characters
    - Normalizing whitespace
    """
    try:
        text = jd_text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)  # remove punctuation
        text = re.sub(r'\s+', ' ', text)      # remove multiple spaces
        return text.strip()
    except Exception as e:
        return f"Error cleaning job description: {e}"
