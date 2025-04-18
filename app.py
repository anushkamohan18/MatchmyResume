import os
import sys
import streamlit as st
from dotenv import load_dotenv

sys.path.append(os.path.abspath("."))

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from utils.resume_parser import extract_resume_text
from utils.jd_parser import clean_job_description
from utils.keyword_extractor import extract_keywords
from utils.match_scorer import compute_match_score
from utils.gpt_feedback import get_gpt_suggestions, get_chat_response
from utils.ats_checker import run_ats_checks
from utils.display_helpers import display_score, display_missing_keywords

# Page settings
st.set_page_config(
    page_title="Resume Match Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    html, body, [class*="css"]  {
        font-family: 'Times New Roman', Times, serif;
        background-color: #0e1117;
        color: #f1f1f1;
    }
    .section-header {
        border-left: 4px solid #4c7bf3;
        padding-left: 12px;
        margin: 1.5rem 0 1rem;
        font-size: 1.3rem;
        font-weight: 600;
    }
    .stTextArea textarea {
        background-color: #1e2630;
        color: #f1f1f1;
        border-radius: 6px;
        font-family: 'Times New Roman', Times, serif;
    }
    .stButton button {
    background-color: #ff5252;
    color: white; /* <-- this makes the text white */
    font-weight: bold;
    border-radius: 50px;
    padding: 0.7rem 2rem;
    font-family: 'Times New Roman', Times, serif;
}

.stButton button:hover {
    background-color: #e64a19;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="top-header">
    <h1>📊 Resume Match Pro</h1>
    <p>Evaluate your resume with AI-powered insights and optional JD matching</p>
</div>
""", unsafe_allow_html=True)

# Upload Resume
st.markdown("<h3 class='section-header'>📄 Upload Resume</h3>", unsafe_allow_html=True)
resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# Mode selection
mode = st.radio("Choose Analysis Mode", ["AI Resume Feedback Only", "With Job Description"], horizontal=True)

jd_text = ""
if mode == "With Job Description":
    st.markdown("<h3 class='section-header'>💼 Paste Job Description</h3>", unsafe_allow_html=True)
    jd_text = st.text_area("Paste JD here", height=180)

analyze_btn = st.button("🔍 Analyze Resume")

if analyze_btn and resume_file:
    with st.spinner("Analyzing resume..."):
        resume_text = extract_resume_text(resume_file)

        # ATS check
        ats_score, ats_warnings = run_ats_checks(resume_text)
        st.markdown("<h3 class='section-header'>📄 ATS Compatibility Check</h3>", unsafe_allow_html=True)
        st.markdown(f"**ATS Score:** {ats_score}/100")
        if ats_warnings:
            st.warning("\n".join(ats_warnings))
        else:
            st.success("Your resume passed common ATS checks.")

        if mode == "With Job Description" and jd_text.strip():
            job_description = clean_job_description(jd_text)
            resume_keywords = extract_keywords(resume_text)
            jd_keywords = extract_keywords(job_description)
            match_score, missing_keywords, category_breakdown = compute_match_score(resume_keywords, jd_keywords)

            st.markdown('<h3 class="section-header">📈 Match Score</h3>', unsafe_allow_html=True)
            display_score(match_score, category_breakdown)

            st.markdown('<h3 class="section-header">🔑 Missing Keywords</h3>', unsafe_allow_html=True)
            display_missing_keywords(missing_keywords)

            st.markdown('<h3 class="section-header">💡 GPT Suggestions</h3>', unsafe_allow_html=True)
            suggestions = get_gpt_suggestions(resume_text, job_description, missing_keywords)
            st.session_state.suggestions = suggestions  # Store for chat context
            st.markdown(f'<div style="background-color: #1e2630; padding: 1rem; border-left: 4px solid #4c7bf3; border-radius: 8px;">{suggestions}</div>', unsafe_allow_html=True)

        else:
            # No JD – general critique
            st.markdown('<h3 class="section-header">💡 AI Resume Review</h3>', unsafe_allow_html=True)
            suggestions = get_gpt_suggestions(resume_text, None, [])
            st.session_state.suggestions = suggestions
            st.markdown(f'<div style="background-color: #1e2630; padding: 1rem; border-left: 4px solid #4c7bf3; border-radius: 8px;">{suggestions}</div>', unsafe_allow_html=True)

            st.markdown('<h3 class="section-header">🗨️ Chat with AI</h3>', unsafe_allow_html=True)
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = [
                    {"role": "system", "content": "You are an assistant helping users improve their resumes. Answer clearly and constructively."},
                    {"role": "assistant", "content": suggestions}
                ]

            user_q = st.text_input("Ask follow-up questions about your resume:", key="chat_input")
            if user_q:
                st.session_state.chat_history.append({"role": "user", "content": user_q})
                response = get_chat_response(st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.markdown(f"**AI:** {response}")

elif analyze_btn:
    st.error("Please upload your resume to continue.")

# Footer
st.markdown("""
<div class="footer">
    Made with ❤️ using Streamlit | Resume Match Pro © 2025
</div>
""", unsafe_allow_html=True)
