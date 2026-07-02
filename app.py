import streamlit as st
import pdfplumber

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📄 AI Resume Analyzer")
st.sidebar.write("### Version 2")
st.sidebar.info(
    """
Upload your resume (PDF) and analyze:
- Resume Score
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
    "Upload your resume to analyze your technical skills and receive feedback."
)

# -----------------------------
# Upload Resume
# -----------------------------
uploaded_file = st.file_uploader(
    "📂 Upload Resume (PDF)",
    type="pdf"
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

    # -------------------------
    # Detect Skills
    # -------------------------
    found = []

    for skill in skills:
        if skill in lower:
            found.append(skill)

    # -------------------------
    # Calculate Score
    # -------------------------
    score = min(len(found) * 12, 100)

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
    # Detected Skills
    # -------------------------
    st.subheader("✅ Detected Skills")

    if found:
        for skill in found:
            st.success(skill.title())
    else:
        st.warning("No matching skills found.")

    # -------------------------
    # Missing Skills
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