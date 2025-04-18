import streamlit as st
import pandas as pd
import altair as alt

def display_score(score: float, category_breakdown: dict):
    """
    Display match score and category-level breakdown + feedback with enhanced visuals.
    Professional Times New Roman styled version.
    """
    # Score display with gauge chart
    cols = st.columns([1, 1])

    with cols[0]:
        st.markdown(f"""
        <div style="text-align: center; font-family: 'Times New Roman', serif;">
            <h2 style="font-size: 1.3rem; color: #d1d5db;">Overall Match Score</h2>
            <div style="font-size: 3.5rem; font-weight: bold; color: {get_score_color(score)};">
                {score}%
            </div>
            <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #adb5bd;">
                {get_score_message(score)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with cols[1]:
        st.markdown(f"""
        <div style="background-color: {get_score_bg_color(score)}; border: 1px solid #4c7bf3; border-radius: 0px; padding: 1rem; height: 100%; font-family: 'Times New Roman', serif;">
            <h3 style="margin-top: 0; color: {get_score_text_color(score)};">Match Analysis</h3>
            <p style="color: {get_score_text_color(score)} !important;">{get_detailed_feedback(score)}</p>
        </div>
        """, unsafe_allow_html=True)

    # Category breakdown
    st.markdown("### 📊 Skill Category Breakdown:")
    breakdown_df = pd.DataFrame({
        'Category': list(category_breakdown.keys()),
        'Coverage': list(category_breakdown.values())
    })

    chart = alt.Chart(breakdown_df).mark_bar().encode(
        x=alt.X('Coverage:Q', axis=alt.Axis(format='%', title='Coverage', titleColor='#d1d5db', labelColor='#d1d5db')),
        y=alt.Y('Category:N', sort='-x', title=None, axis=alt.Axis(labelColor='#d1d5db')),
        color=alt.Color('Coverage:Q', scale=alt.Scale(
            domain=[0, 40, 70, 100],
            range=['#f44336', '#ff9800', '#4caf50', '#2e7d32']
        )),
        tooltip=['Category', alt.Tooltip('Coverage:Q', format='.1f')]
    ).properties(
        height=len(category_breakdown) * 40
    ).configure_view(
        strokeWidth=0
    )

    st.altair_chart(chart, use_container_width=True)

    st.markdown("### 🧠 Skill Insights:")
    for category, percent in category_breakdown.items():
        if percent >= 70:
            st.markdown(f"""
            <div style="font-family: 'Times New Roman', serif; display: flex; align-items: center; margin-bottom: 0.5rem; background-color: #263238; padding: 0.75rem; border: 1px solid #4caf50;">
                <div style="background-color: #4caf50; color: white; width: 24px; height: 24px; border-radius: 0px; text-align: center; margin-right: 10px;">✓</div>
                <div><strong>{category}</strong>: {percent}% - <span style="color: #81c784;">Strong coverage</span></div>
            </div>
            """, unsafe_allow_html=True)
        elif 40 <= percent < 70:
            st.markdown(f"""
            <div style="font-family: 'Times New Roman', serif; display: flex; align-items: center; margin-bottom: 0.5rem; background-color: #2c2c2c; padding: 0.75rem; border: 1px solid #ff9800;">
                <div style="background-color: #ff9800; color: white; width: 24px; height: 24px; border-radius: 0px; text-align: center; margin-right: 10px;">⚠</div>
                <div><strong>{category}</strong>: {percent}% - <span style="color: #ffb74d;">Could be improved</span></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="font-family: 'Times New Roman', serif; display: flex; align-items: center; margin-bottom: 0.5rem; background-color: #2d2626; padding: 0.75rem; border: 1px solid #f44336;">
                <div style="background-color: #f44336; color: white; width: 24px; height: 24px; border-radius: 0px; text-align: center; margin-right: 10px;">✗</div>
                <div><strong>{category}</strong>: {percent}% - <span style="color: #e57373;">Needs significant improvement</span></div>
            </div>
            """, unsafe_allow_html=True)

def display_missing_keywords(missing_keywords: list):
    if missing_keywords:
        st.markdown("""
        <div style="font-family: 'Times New Roman', serif; background-color: #2d2a20; padding: 1rem; border: 1px solid #4c7bf3;">
            <h3 style="margin-top: 0; color: #f1f1f1;">Missing Keywords</h3>
            <p style="color: #d1d5db;">These keywords from the job description weren't found in your resume:</p>
        </div>
        """, unsafe_allow_html=True)
        keyword_html = ""
        for kw in missing_keywords:
            keyword_html += f'<span style="display: inline-block; background-color: #3a3426; color: #ffecb3; padding: 0.4rem 0.8rem; margin: 0.3rem; border: 1px solid #ffecb3; font-size: 0.9rem; font-family: Times New Roman, serif;">{kw}</span>'
        st.markdown(f"""
        <div style="margin-top: 1rem;">{keyword_html}</div>
        <div style="margin-top: 1rem; font-size: 0.9rem; color: #adb5bd; font-family: Times New Roman, serif;">
            Consider incorporating these keywords into your resume to improve your match score.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color: #263238; padding: 1rem; border: 1px solid #4caf50; text-align: center; font-family: Times New Roman, serif;">
            <h3 style="margin-top: 0; color: #81c784;">🎯 Perfect Keyword Match!</h3>
            <p style="color: #d1d5db;">Your resume includes all the important keywords from the job description.</p>
        </div>
        """, unsafe_allow_html=True)

def get_score_color(score: float) -> str:
    if score >= 80:
        return "#81c784"
    elif score >= 60:
        return "#64b5f6"
    elif score >= 40:
        return "#ffb74d"
    else:
        return "#e57373"

def get_score_bg_color(score: float) -> str:
    if score >= 80:
        return "#263238"
    elif score >= 60:
        return "#1e3246"
    elif score >= 40:
        return "#3d3226"
    else:
        return "#3b2626"

def get_score_text_color(score: float) -> str:
    if score >= 80:
        return "#81c784"
    elif score >= 60:
        return "#64b5f6"
    elif score >= 40:
        return "#ffb74d"
    else:
        return "#e57373"

def get_score_message(score: float) -> str:
    if score >= 80:
        return "Excellent Match"
    elif score >= 60:
        return "Good Match"
    elif score >= 40:
        return "Fair Match"
    else:
        return "Needs Improvement"

def get_detailed_feedback(score: float) -> str:
    if score >= 80:
        return "Your resume is very well-aligned with this job description. You are likely to pass automated resume screening systems (ATS) and catch the recruiter's attention."
    elif score >= 60:
        return "Your resume matches this job well but could be further optimized. With some targeted adjustments, you can significantly improve your chances."
    elif score >= 40:
        return "Your resume partially matches the job requirements. Consider significant revisions to better highlight relevant skills and experience."
    else:
        return "Your resume needs substantial changes to align with this job. Focus on adding missing keywords and restructuring to emphasize relevant experience."
