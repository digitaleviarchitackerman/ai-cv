import streamlit as st
from docx import Document
from PyPDF2 import PdfFileReader
import io

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfFileReader(file)
    text = ""
    for page in range(reader.getNumPages()):
        text += reader.getPage(page).extract_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to process and edit CV based on JD
def edit_cv(jd, cv_text):
    # Here, you can implement the logic to edit the CV based on the JD
    # For simplicity, this example just appends the JD to the CV
    edited_cv = cv_text + "\n\n" + "JD:" + jd
    return edited_cv

st.title("NaviAI AI CV")

# Input CV
cv_option = st.radio("Input CV", ("Upload File", "Paste Text"))

if cv_option == "Upload File":
    cv_file = st.file_uploader("Upload CV file", type=["pdf", "docx"])
    if cv_file:
        if cv_file.type == "application/pdf":
            cv_text = extract_text_from_pdf(cv_file)
        else:
            cv_text = extract_text_from_docx(cv_file)
else:
    cv_text = st.text_area("Paste CV text here")

# Input JD
jd_option = st.radio("Input Job Description (JD)", ("Upload File", "Paste Text"))

if jd_option == "Upload File":
    jd_file = st.file_uploader("Upload JD file", type=["pdf", "docx"])
    if jd_file:
        if jd_file.type == "application/pdf":
            jd = extract_text_from_pdf(jd_file)
        else:
            jd = extract_text_from_docx(jd_file)
else:
    jd = st.text_area("Paste JD text here")

if st.button("Submit"):
    if jd and cv_text:
        edited_cv = edit_cv(jd, cv_text)
        # Create a downloadable DOCX file
        doc = Document()
        for line in edited_cv.split("\n"):
            doc.add_paragraph(line)
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        st.download_button("Download Edited CV", buffer, "edited_cv.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    else:
        st.warning("Please provide both JD and CV.")
