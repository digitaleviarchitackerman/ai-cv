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
        children = tag.find_all(recursive=False)
        if children:
            inner_html = ''.join([wrap_with_div(child) for child in children])
            return f'<div class="{tag.name}">{inner_html}</div>'
        else:
            return f'<div class="{tag.name}">{tag.text}</div>'

    for tag in soup.find_all(recursive=False):
        html_content += wrap_with_div(tag)

    return f"<html><body>{html_content}</body></html>"

# Streamlit app
with st.sidebar:
    st.header("Input Section")
    
    # Input CV
    cv_text = st.text_area("Paste CV text here")

    # Input JD
    jd = st.text_area("Paste JD text here")

if st.sidebar.button("Submit"):
    if jd and cv_text:
        cv_data = get_edited_cv(cv_text, jd)
        if isinstance(cv_data, str):  # Check if the returned data is the XML string
            html_content = xml_to_html(cv_data)
            st.subheader("Generated XML")
            st.code(cv_data, language="xml")
            st.subheader("Generated HTML")
            st.code(html_content, language="html")
            st.download_button(
                label="Download HTML",
                data=html_content,
                file_name="edited_cv.html",
                mime="text/html"
            )
        else:
            st.error("Failed to get edited CV from the API.")
            st.json(cv_data)  # Display the whole response for debugging
    else:
        st.warning("Please provide both JD and CV.")
