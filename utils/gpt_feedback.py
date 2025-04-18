import os
from openai import OpenAI
from typing import List, Optional

def _init_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)

def get_gpt_suggestions(resume_text: str, jd_text: Optional[str], missing_keywords: List[str]) -> str:
    """
    Uses GPT to suggest improvements based on missing keywords and job description context.
    If no JD is provided, generates general resume enhancement suggestions.
    """
    client = _init_client()

    if jd_text:
        prompt = (
            "You are a resume optimization assistant. "
            "Given the candidate's resume, the job description, and a list of missing keywords, "
            "provide 3–5 suggestions to improve the resume. Be specific and professional.\n\n"
            f"Missing Keywords:\n{', '.join(missing_keywords)}\n\n"
            f"Job Description:\n{jd_text}\n\n"
            f"Resume:\n{resume_text}\n\n"
            "Suggestions:"
        )
    else:
        prompt = (
            "You are a resume optimization assistant. "
            "Given the candidate's resume, provide 3–5 suggestions to improve it for general job applications. "
            "Focus on clarity, formatting, impact, and alignment with typical job requirements.\n\n"
            f"Resume:\n{resume_text}\n\n"
            "Suggestions:"
        )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful resume critique assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ GPT suggestion error: {e}"

def get_chat_response(chat_history: List[dict]) -> str:
    """
    Handles follow-up questions as a conversational chatbot using existing chat history.
    """
    client = _init_client()

    if not chat_history or chat_history[0].get("role") != "system":
        chat_history.insert(0, {
            "role": "system",
            "content": "You are an assistant helping users improve their resumes. Answer clearly and constructively."
        })

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            temperature=0.5,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ GPT chat error: {e}"
