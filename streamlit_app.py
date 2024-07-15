import streamlit as st
import requests
import json
import re
from docx import Document
from PyPDF2 import PdfReader
import io

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to call the API and get the edited CV
def get_edited_cv(cv_text, jd):
    # Define the URL for the API endpoint
    url = "https://api.coze.com/open_api/v2/chat"

    # Define the headers for the API request
    headers = {
        "Authorization": "Bearer pat_tdxTFe1O5DrjQJsmO6gEuyKmxz8DzyvyIpAMA6faYmgDHMpaTGIXEVoZptMWC27M",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Host": "api.coze.com",
        "Connection": "keep-alive"
    }

    # Define the data to be sent with the API request
    query = f"CV: {cv_text} JD: {jd}"
    data = {
        "conversation_id": "123",
        "bot_id": "7388896804592746497",
        "user": "123333333",
        "query": f"Give me my json CV knowing that:\n{query}",
        "stream": False
    }

    # Send a POST request to the API endpoint
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Get the response from the API request
    response_json = response.json()

    # Iterate over the messages in the response
    for message in response_json['messages']:
        # If the role is 'assistant' and the type is 'answer', parse the JSON in the content
        if message['role'] == 'assistant' and message['type'] == 'answer':
            json_match = re.search(r'\{.*\}', message['content'], re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
    return None

# Function to generate markdown from the CV data
def generate_markdown(cv_data):
    md_content = []

    # Header
    header = cv_data.get("header", {})
    name = header.get("name", "")
    contact = header.get("contact", {})
    email = contact.get("email", "")
    phone = contact.get("phone", "")
    linkedin = contact.get("linkedin", "")
    github = contact.get("github", "")
    personal_website = contact.get("personal_website", "")
    
    if name:
        md_content.append(f"# {name}")
    if email:
        md_content.append(f"- **Email:** {email}")
    if phone:
        md_content.append(f"- **Phone:** {phone}")
    if linkedin:
        md_content.append(f"- **LinkedIn:** [{linkedin}]({linkedin})")
    if github:
        md_content.append(f"- **GitHub:** [{github}]({github})")
    if personal_website:
        md_content.append(f"- **Website:** [{personal_website}]({personal_website})")
    
    # Summary
    summary = cv_data.get("summary", "")
    if summary:
        md_content.append("\n## Summary\n")
        md_content.append(summary)
    
    # Education
    education = cv_data.get("education", [])
    if education:
        md_content.append("\n## Education\n")
        for edu in education:
            institution = edu.get("institution", "")
            location = edu.get("location", "")
            degree = edu.get("degree", "")
            dates = edu.get("dates", "")
            details = edu.get("details", {})
            honors = details.get("honors", [])
            relevant_courses = details.get("relevant_courses", [])
            
            if institution:
                md_content.append(f"**{institution}**, {location}")
                if degree:
                    md_content.append(f"- **Degree:** {degree}")
                if dates:
                    md_content.append(f"- **Dates:** {dates}")
                if honors:
                    md_content.append(f"- **Honors:** {', '.join(honors)}")
                if relevant_courses:
                    md_content.append(f"- **Relevant Courses:** {', '.join(relevant_courses)}")
    
    # Professional Experience
    professional_experience = cv_data.get("professional_experience", [])
    if professional_experience:
        md_content.append("\n## Professional Experience\n")
        for exp in professional_experience:
            company = exp.get("company", "")
            location = exp.get("location", "")
            role = exp.get("role", "")
            dates = exp.get("dates", "")
            responsibilities = exp.get("responsibilities", [])
            
            if company:
                md_content.append(f"**{company}**, {location}")
                if role:
                    md_content.append(f"- **Role:** {role}")
                if dates:
                    md_content.append(f"- **Dates:** {dates}")
                if responsibilities:
                    for responsibility in responsibilities:
                        md_content.append(f"  - {responsibility}")
    
    # Research Experience
    research_experience = cv_data.get("research_experience", [])
    if research_experience:
        md_content.append("\n## Research Experience\n")
        for research in research_experience:
            institution = research.get("institution", "")
            location = research.get("location", "")
            role = research.get("role", "")
            dates = research.get("dates", "")
            responsibilities = research.get("responsibilities", [])
            
            if institution:
                md_content.append(f"**{institution}**, {location}")
                if role:
                    md_content.append(f"- **Role:** {role}")
                if dates:
                    md_content.append(f"- **Dates:** {dates}")
                if responsibilities:
                    for responsibility in responsibilities:
                        md_content.append(f"  - {responsibility}")
    
    # Publications
    publications = cv_data.get("publications", [])
    if publications:
        md_content.append("\n## Publications\n")
        for pub in publications:
            authors = pub.get("authors", "")
            title = pub.get("title", "")
            journal_or_conference = pub.get("journal_or_conference", "")
            date = pub.get("date", "")
            link = pub.get("link", "")
            details = pub.get("details", {})
            media_coverage = details.get("media_coverage", [])
            presentations = details.get("presentations", [])
            
            if title:
                md_content.append(f"- **{title}**")
                if authors:
                    md_content.append(f"  - **Authors:** {authors}")
                if journal_or_conference:
                    md_content.append(f"  - **Journal/Conference:** {journal_or_conference}")
                if date:
                    md_content.append(f"  - **Date:** {date}")
                if link:
                    md_content.append(f"  - **Link:** [{link}]({link})")
                if media_coverage:
                    md_content.append(f"  - **Media Coverage:** {', '.join(media_coverage)}")
                if presentations:
                    md_content.append(f"  - **Presentations:** {', '.join(presentations)}")
    
    # Projects
    projects = cv_data.get("projects", [])
    if projects:
        md_content.append("\n## Projects\n")
        for project in projects:
            name = project.get("name", "")
            dates = project.get("dates", "")
            description = project.get("description", "")
            technologies_used = project.get("technologies_used", [])
            
            if name:
                md_content.append(f"**{name}**")
                if dates:
                    md_content.append(f"- **Dates:** {dates}")
                if description:
                    md_content.append(f"- **Description:** {description}")
                if technologies_used:
                    md_content.append(f"- **Technologies Used:** {', '.join(technologies_used)}")
    
    # Technical Skills
    technical_skills = cv_data.get("technical_skills", {})
    if technical_skills:
        md_content.append("\n## Technical Skills\n")
        for skill_category, skills in technical_skills.items():
            if skills:
                md_content.append(f"- **{skill_category.replace('_', ' ').title()}:** {', '.join(skills)}")
    
    # Honors and Awards
    honors_and_awards = cv_data.get("honors_and_awards", [])
    if honors_and_awards:
        md_content.append("\n## Honors and Awards\n")
        for award in honors_and_awards:
            title = award.get("title", "")
            organization = award.get("organization", "")
            date = award.get("date", "")
            
            if title:
                md_content.append(f"- **{title}**")
                if organization:
                    md_content.append(f"  - **Organization:** {organization}")
                if date:
                    md_content.append(f"  - **Date:** {date}")
    
    # Teaching Experience
    teaching_experience = cv_data.get("teaching_experience", [])
    if teaching_experience:
        md_content.append("\n## Teaching Experience\n")
        for teaching in teaching_experience:
            institution = teaching.get("institution", "")
            course = teaching.get("course", "")
            role = teaching.get("role", "")
            dates = teaching.get("dates", "")
            
            if institution:
                md_content.append(f"**{institution}**")
                if course:
                    md_content.append(f"- **Course:** {course}")
                if role:
                    md_content.append(f"- **Role:** {role}")
                if dates:
                    md_content.append(f"- **Dates:** {dates}")
    
    # Service and Leadership
    service_and_leadership = cv_data.get("service_and_leadership", [])
    if service_and_leadership:
        md_content.append("\n## Service and Leadership\n")
        for service in service_and_leadership:
            organization = service.get("organization", "")
            role = service.get("role", "")
            dates = service.get("dates", "")
            
            if organization:
                md_content.append(f"**{organization}**")
                if role:
                    md_content.append(f"- **Role:** {role}")
                if dates:
                    md_content.append(f"- **Dates:** {dates}")
    
    # Mentorship
    mentorship = cv_data.get("mentorship", [])
    if mentorship:
        md_content.append("\n## Mentorship\n")
        for mentor in mentorship:
            organization = mentor.get("organization", "")
            role = mentor.get("role", "")
            dates = mentor.get("dates", "")
            
            if organization:
                md_content.append(f"**{organization}**")
                if role:
                    md_content.append(f"- **Role:** {role}")
                if dates:
                    md_content.append(f"- **Dates:** {dates}")
    
    # Talks and Presentations
    talks_and_presentations = cv_data.get("talks_and_presentations", [])
    if talks_and_presentations:
        md_content.append("\n## Talks and Presentations\n")
        for talk in talks_and_presentations:
            title = talk.get("title", "")
            event = talk.get("event", "")
            date = talk.get("date", "")
            
            if title:
                md_content.append(f"- **{title}**")
                if event:
                    md_content.append(f"  - **Event:** {event}")
                if date:
                    md_content.append(f"  - **Date:** {date}")
    
    # Media Coverage
    media_coverage = cv_data.get("media_coverage", [])
    if media_coverage:
        md_content.append("\n## Media Coverage\n")
        for media in media_coverage:
            title = media.get("title", "")
            media_outlet = media.get("media_outlet", "")
            date = media.get("date", "")
            
            if title:
                md_content.append(f"- **{title}**")
                if media_outlet:
                    md_content.append(f"  - **Media Outlet:** {media_outlet}")
                if date:
                    md_content.append(f"  - **Date:** {date}")

    return "\n".join(md_content)

# Streamlit app
with st.sidebar:
    st.header("Input Section")
    
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

if st.sidebar.button("Submit"):
    if jd and cv_text:
        cv_data = get_edited_cv(cv_text, jd)
        if cv_data:
            markdown_content = generate_markdown(cv_data)
            st.markdown(markdown_content)
        else:
            st.error("Failed to get edited CV from the API.")
    else:
        st.warning("Please provide both JD and CV.")
