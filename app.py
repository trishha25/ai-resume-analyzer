import streamlit as st
import pdfplumber

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📄 AI Resume Analyzer")
st.sidebar.write("### Version 3")
st.sidebar.info(
    """
Upload your resume (PDF) and analyze:
- Resume Score
- ATS Match
- Technical Skills
- Missing Skills
- Resume Feedback
"""
)

# -----------------------------
# Skills Database
# -----------------------------
skills = [
    "python",
    "machine learning",
    "deep learning",
    "power bi",
    "excel",
    "statistics",
    "llm",
    "prompt engineering"
]

# -----------------------------
# Main Title
# -----------------------------
st.title("🤖 AI Resume Analyzer")

st.write(
    "Upload your resume to analyze your technical skills and compare it with a job description."
)

# -----------------------------
# Upload Resume
# -----------------------------
uploaded_file = st.file_uploader(
    "📂 Upload Resume (PDF)",
    type="pdf"
)

# -----------------------------
# Job Description
# -----------------------------
st.subheader("📝 Job Description")

job_description = st.text_area(
    "Paste the Job Description Here",
    height=200,
    placeholder="""Example:

Looking for an AI/ML Intern

Required Skills:
Python
Machine Learning
SQL
Power BI
Git
Deep Learning
"""
)

# -----------------------------
# Resume Analysis
# -----------------------------
if uploaded_file:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

    lower = text.lower()
    job_lower = job_description.lower()

    # -------------------------
    # Detect Skills
    # -------------------------
    found = []
    matched = []
    missing_keywords = []

    for skill in skills:

        if skill in lower:
            found.append(skill)

        if skill in lower and skill in job_lower:
            matched.append(skill)

        elif skill in job_lower:
            missing_keywords.append(skill)

    # -------------------------
    # Resume Score
    # -------------------------
    score = min(len(found) * 12, 100)

    # -------------------------
    # ATS Score
    # -------------------------
    ats_score = 0

    if job_description.strip():

        total_required = len(matched) + len(missing_keywords)

        if total_required > 0:
            ats_score = int(
                (len(matched) / total_required) * 100
            )

    # -------------------------
    # Resume Score
    # -------------------------
    st.subheader("📊 Resume Score")

    st.progress(score)

    st.metric(
        label="Overall Score",
        value=f"{score}%"
    )

    # -------------------------
    # ATS Match
    # -------------------------
    if job_description.strip():

        st.subheader("🎯 ATS Match")

        st.progress(ats_score)

        st.metric(
            label="ATS Match",
            value=f"{ats_score}%"
        )

    # -------------------------
    # Detected Skills
    # -------------------------
    st.subheader("✅ Detected Skills")

    if found:
        for skill in found:
            st.success(skill.title())
    else:
        st.warning("No matching skills found.")

    # -------------------------
    # Recommended Skills
    # -------------------------
    missing = []

    for skill in skills:
        if skill not in found:
            missing.append(skill)

    st.subheader("📌 Recommended Skills")

    if missing:
        for skill in missing:
            st.warning(f"Learn {skill.title()}")
    else:
        st.success("Excellent! No missing skills detected.")

    # -------------------------
    # Missing Keywords (ATS)
    # -------------------------
    if job_description.strip():

        st.subheader("❌ Missing Keywords")

        if missing_keywords:

            for skill in missing_keywords:
                st.error(skill.title())

        else:
            st.success("Your resume contains all required keywords.")

    # -------------------------
    # Resume Feedback
    # -------------------------
    st.subheader("💬 Feedback")

    if score >= 80:

        st.balloons()

        st.success(
            """
Excellent Resume!

Your resume contains many important AI and Analytics skills.

Keep building projects and internships.
"""
        )

    elif score >= 50:

        st.warning(
            """
Good Resume!

Add more AI/ML projects, certifications, and technical skills to improve your profile.
"""
        )

    else:

        st.error(
            """
Your resume needs improvement.

Consider adding:
- More technical skills
- AI/ML projects
- Certifications
- GitHub profile
"""
        )

    # -------------------------
    # Resume Preview
    # -------------------------
    with st.expander("📄 Resume Preview"):
        st.write(text)