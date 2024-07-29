import streamlit as st
import requests
import json
import re
from bs4 import BeautifulSoup

# Function to call the API and get the edited CV in XML format
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
    query = f"My CV: {cv_text} My JD: {jd}"
    data = {
        "bot_id": "7396141067857002514",
        "user": "aicv",
        "query": f"{query}",
        "stream": False
    }

    # Send a POST request to the API endpoint
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Get the response from the API request
    response_json = response.json()

    # Iterate over the messages in the response
    for message in response_json['messages']:
        # If the role is 'assistant' and the type is 'answer', parse the XML in the content
        if message['role'] == 'assistant' and message['type'] == 'answer':
            xml_match = re.search(r'<.*>', message['content'], re.DOTALL)
            if xml_match:
                return xml_match.group()
    return response_json  # Return the whole response for debugging

# Function to convert XML to HTML
def xml_to_html(xml_content):
    soup = BeautifulSoup(xml_content, 'xml')
    html_content = ''

    def wrap_with_div(tag):
        if tag.name is None:  # If it's a string/text node, return it as-is
            return str(tag)
        inner_html = ''.join([wrap_with_div(child) for child in tag.children])
        return f'<div class="{tag.name}">{inner_html}</div>'

    for tag in soup.contents:
        if tag.name:  # Ensure it's an element and not a text node
            html_content += wrap_with_div(tag)

    head_content = '''
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: "Times New Roman", Times, serif;
                margin: 20px;
            }
            .cv {
                width: 100%;
            }
            .cvHeader {
                text-align: center;
                font-size: 1.2em;
                font-weight: bold;
            }
            .cvHeader .firstName, .cvHeader .lastName {
                display: inline-block;
                text-align: center;
            }
            .cvHeader .contacts {
                margin-top: 5px;
            }
            .cvHeader .contacts .li {
                display: inline;
                margin-right: 5px;
            }
            .cvHeader .separator {
                display: inline;
                margin: 0 5px;
            }
            .cvBody {
                margin-top: 20px;
            }
            .section {
                margin-bottom: 20px;
            }
            .sectionName {
                font-size: 1.1em;
                font-weight: bold;
                text-transform: uppercase;
                border-bottom: 1px solid #000;
                margin-bottom: 10px;
            }
            .institution, .experience, .award, .skill {
                margin-bottom: 10px;
            }
            .name, .organization, .project, .awardName, .skillName {
                font-weight: bold;
            }
            .location, .date, .position, .title {
                display: inline-block;
                font-style: italic;
                margin-right: 10px;
            }
            .location {
                float: right;
                text-align: right;
            }
            .date {
                float: right;
                text-align: right;
                clear: both;
            }
            .bulletPoints .li {
                margin-left: 20px;
                clear: both;
                position: relative;
            }
            .bulletPoints .li::before {
                content: "•";
                position: absolute;
                left: -20px;
                font-size: 1.2em;
            }
            .bulletPoints {
                list-style-type: none;
                padding-left: 20px;
            }
            .skillSets .li {
                display: inline;
            }
            .skillSets .li:not(:last-child)::after {
                content: ",";
            }
        </style>
        <title>CV</title>
      </head>
    '''

    return f"{head_content}<body contenteditable='true'>{html_content}</body></html>"

# Streamlit app
with st.sidebar:
    st.header("V2.2")
    
    # Input CV
    cv_text = st.text_area("Paste CV text here")

    # Input JD
    jd = st.text_area("Paste JD text here")

if st.sidebar.button("Submit"):
    if jd and cv_text:
        cv_data = get_edited_cv(cv_text, jd)
        if isinstance(cv_data, str):  # Check if the returned data is the XML string
            html_content = xml_to_html(cv_data)
            st.download_button(
                label="Download HTML",
                data=html_content,
                file_name="edited_cv.html",
                mime="text/html"
            )
            st.subheader("Generated XML")
            st.code(cv_data, language="xml")
            st.subheader("Generated HTML")
            st.code(html_content, language="html")
        else:
            st.error("Failed to get edited CV from the API.")
            st.json(cv_data)  # Display the whole response for debugging
    else:
        st.warning("Please provide both JD and CV.")
