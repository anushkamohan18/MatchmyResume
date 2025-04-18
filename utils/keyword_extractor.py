import spacy
import os
from typing import List
from openai import OpenAIError
from langchain_community.embeddings import OpenAIEmbeddings
from openai import OpenAI

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

USE_GPT_FALLBACK = True  # Set this to False if you want to disable GPT fallback


def extract_keywords(text: str, use_gpt=USE_GPT_FALLBACK) -> List[str]:
    """
    Extracts keywords from text using spaCy (default) and falls back to GPT if enabled.
    """
    keywords = extract_with_spacy(text)

    if not keywords and use_gpt:
        try:
            keywords = extract_with_gpt(text)
        except OpenAIError as e:
            print(f"OpenAI API error: {e}")
            keywords = []

    return list(set([kw.lower().strip() for kw in keywords]))


def extract_with_spacy(text: str) -> List[str]:
    """
    Uses spaCy to extract nouns and verbs as rough 'keywords'.
    """
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN', 'VERB'] and len(token.text) > 2]
    return keywords


def extract_with_gpt(text: str) -> List[str]:
    """
    Uses OpenAI to extract keywords from the text (fallback method).
    """
    from openai import OpenAI

    client = OpenAI()

    prompt = (
        "Extract the most relevant skills, tools, and keywords from this text. "
        "Return them as a Python list of lowercase strings:\n\n"
        f"{text}\n\nKeywords:"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=100,
    )

    # Safely eval the result (expects a Python-style list string)
    raw_output = response.choices[0].message.content
    keywords = eval(raw_output.strip()) if "[" in raw_output else []
    return keywords
