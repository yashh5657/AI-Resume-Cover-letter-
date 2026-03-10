import streamlit as st
from fpdf import FPDF
from io import BytesIO
import re

st.set_page_config(page_title="ATS Resume Generator")

st.title("📄 ATS Resume & Cover Letter Generator")
st.write("Fill your details and generate an ATS-friendly resume and cover letter in PDF format.")

# User inputs
name = st.text_input("Full Name").strip()
email = st.text_input("Email").strip()
phone = st.text_input("Phone Number").strip()
skills = st.text_area("Skills").strip()
experience = st.text_area("Experience").strip()
education = st.text_area("Education").strip()
certifications = st.text_area("Certifications").strip()
job_role = st.text_input("Job Role Applying For").strip()

# Template selection
template_choice = st.radio(
    "Choose a Resume Template",
    ("Chronological ATS", "Skills-Based ATS")
)

# Sanitize text to remove non-ASCII characters
def sanitize(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

if st.button("Generate PDF"):
    if not name or not email or not job_role:
        st.error("Please fill in at least your name, email, and job role.")
    else:
        # Fallbacks
        skills = skills if skills else "Not specified"
        experience = experience if experience else "Not specified"
        education = education if education else "Not specified"
        certifications = certifications if certifications else "Not specified"

        # Template 1: Chronological ATS (Experience-first)
        if template_choice == "Chronological ATS":
            summary = f"{name} is a motivated professional skilled in {skills}. With experience in {experience}, {name} is applying for the role of {job_role}."
            resume = f"""
Job Role Applying For: {job_role}

------------------------------------
Professional Summary
------------------------------------
{summary}

------------------------------------
Experience
------------------------------------
{experience}

------------------------------------
Skills
------------------------------------
{skills}

------------------------------------
Education
------------------------------------
{education}

------------------------------------
Certifications
------------------------------------
{certifications}
"""
            cover_letter = f"""
Dear Hiring Manager,

I am writing to apply for the position of {job_role}. My name is {name}, and I have strong skills in {skills}.
With experience in {experience}, I believe I can contribute effectively to your organization.

Thank you for considering my application.

Sincerely,
{name}
"""

        # Template 2: Skills-Based ATS (Skills-first)
        else:
            resume = f"""
Job Role Applying For: {job_role}

====================================
Key Skills
====================================
{skills}

====================================
Professional Experience
====================================
{experience}

====================================
Education
====================================
{education}

====================================
Certifications
====================================
{certifications}

====================================
Summary
====================================
{name} brings expertise in {skills} and proven experience in {experience}.
Seeking to contribute effectively in the role of {job_role}.
"""
            cover_letter = f"""
Dear Hiring Manager,

I am excited to apply for the role of {job_role}. My background in {experience} 
and expertise in {skills} make me a strong candidate for this position.

I am confident that my skills and dedication will add value to your team.

Best regards,
{name}
"""

        # Sanitize content
        resume = sanitize(resume)
        cover_letter = sanitize(cover_letter)

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()

        # 🔹 Big bold name at top
        pdf.set_font("Arial", style="B", size=20)
        pdf.cell(0, 12, name.upper(), ln=True, align="C")

        pdf.ln(5)

        # 🔹 Bold Email & Phone
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(0, 10, f"Email: {email} | Phone: {phone}", ln=True, align="C")

        pdf.ln(5)

        # Resume content
        pdf.set_font("Arial", size=12)
        for line in resume.split("\n"):
            pdf.multi_cell(0, 8, line)

        # Cover Letter Page
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(0, 12, "Cover Letter", ln=True, align="C")

        pdf.ln(5)
        pdf.set_font("Arial", size=12)
        for line in cover_letter.split("\n"):
            pdf.multi_cell(0, 8, line)

        # Safe output
        pdf_bytes = pdf.output(dest="S").encode("latin-1", errors="ignore")
        buffer = BytesIO(pdf_bytes)

        st.download_button(
            label="Download Resume & Cover Letter PDF",
            data=buffer,
            file_name="resume_cover_letter.pdf",
            mime="application/pdf"
        )
        st.success("PDF Generated Successfully!")
