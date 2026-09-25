import streamlit as st
from src.config import Config
from src.pdf_parser import DocumentParser
from src.llm_client import GroqLLMClient
from src.report_generator import PDFReportGenerator
from src.utils import render_custom_css, display_badges

st.set_page_config(
    page_title="Enterprise AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

render_custom_css()

# Sidebar
with st.sidebar:
    st.title("Settings & Info")
    st.info("Upload your resume and a target Job Description to receive an evaluation, skill gap analysis, and tailored interview questions.")
    model_choice = st.text_input("Active Groq Model", value=Config.GROQ_MODEL, disabled=True)

st.title("AI Resume Analyzer & Job Matcher")
st.caption("Powered by Groq LLM Infrastructure")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Resume Upload")
    uploaded_file = st.file_uploader("Upload PDF or DOCX format", type=["pdf", "docx"])

with col2:
    st.subheader("2. Job Description")
    job_description = st.text_area("Paste job responsibilities & requirements", height=200)

analyze_btn = st.button("Analyze Match", type="primary", use_container_width=True)

if analyze_btn:
    if not uploaded_file:
        st.error("Please upload a resume file.")
        st.stop()
    if not job_description.strip():
        st.error("Please provide a job description.")
        st.stop()

    try:
        with st.spinner("Extracting document contents..."):
            resume_text = DocumentParser.extract_text(uploaded_file)

        if len(resume_text) < 50:
            st.error("Could not extract sufficient text from the document. Please verify the document format.")
            st.stop()

        with st.spinner("Analyzing profile against requirements using Groq..."):
            client = GroqLLMClient()
            report = client.analyze_resume(resume_text, job_description)

        st.session_state["report"] = report
        st.session_state["resume_text"] = resume_text

    except Exception as e:
        st.error(f"Execution Error: {str(e)}")

if "report" in st.session_state:
    report = st.session_state["report"]

    st.divider()
    st.header("Analysis Overview")

    m1, m2, m3 = st.columns(3)
    m1.metric("ATS Alignment Score", f"{report.ats_score}%")
    m2.metric("Matched Skills Count", len(report.matched_skills))
    m3.metric("Missing Skills Count", len(report.missing_skills))

    st.progress(report.ats_score / 100.0)

    st.subheader("Candidate Overview")
    st.write(report.candidate_summary)

    st.divider()

    # Skills Breakdown
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown("### Matched Skills")
        display_badges(report.matched_skills, "matched")
    with sc2:
        st.markdown("### Partial / Related")
        display_badges(report.partial_match_skills, "partial")
    with sc3:
        st.markdown("### Missing Skills")
        display_badges(report.missing_skills, "missing")

    st.divider()

    # Detailed Alignments
    ec1, ec2, ec3 = st.columns(3)
    with ec1:
        st.markdown("### Experience Alignment")
        st.write(report.experience_match)
    with ec2:
        st.markdown("### Education Alignment")
        st.write(report.education_match)
    with ec3:
        st.markdown("### Projects Alignment")
        st.write(report.project_match)

    st.divider()

    # Improvements & Questions
    ic1, ic2 = st.columns(2)
    with ic1:
        st.markdown("### Recommended Action Items")
        for idx, imp in enumerate(report.resume_improvements, 1):
            st.markdown(f"**{idx}.** {imp}")
    with ic2:
        st.markdown("### Generated Interview Questions")
        for idx, q in enumerate(report.interview_questions, 1):
            st.markdown(f"**{idx}.** {q}")

    st.divider()

    # PDF Export Section
    pdf_buffer = PDFReportGenerator.generate_pdf(report)
    st.download_button(
        label="Download Full PDF Analysis",
        data=pdf_buffer,
        file_name="ATS_Resume_Analysis.pdf",
        mime="application/pdf",
        type="secondary"
    )