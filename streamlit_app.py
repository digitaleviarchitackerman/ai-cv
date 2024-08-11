import streamlit as st
import requests
import json
import re
from bs4 import BeautifulSoup

# Load secrets
api_key = st.secrets["api_key"]
bot_id = st.secrets["bot_id"]
head_content = st.secrets["head_content"]["head_html"]

# Function to call the API and get the edited CV in XML format
def get_edited_cv(cv_text, jd):
    # Define the URL for the API endpoint
    url = "https://api.coze.com/open_api/v2/chat"

    # Define the headers for the API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Host": "api.coze.com",
        "Connection": "keep-alive"
    }

    # Define the data to be sent with the API request
    query = f"My CV: {cv_text} My JD: {jd}"
    data = {
        "bot_id": bot_id,
        "user": "naviai",
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

    return f"{head_content}<body contenteditable='true'>{html_content}</body></html>"

# Streamlit app
st.header("V2.4.0")
st.sidebar.header("NaviAI CV")
st.sidebar.text(f"Number of CVs generated: {get_cv_count()}")

# Input CV
cv_text = st.sidebar.text_area("Paste CV text here")

# Input JD
jd = st.sidebar.text_area("Paste JD text here")

if st.sidebar.button("Submit"):
    if jd and cv_text:
        cv_data = get_edited_cv(cv_text, jd)
        if isinstance(cv_data, str):  # Check if the returned data is the XML string
            increment_cv_count()
            html_content = xml_to_html(cv_data)
            print("Generated XML:\n", cv_data)  # Print XML for debugging
            print("Generated HTML:\n", html_content)  # Print HTML for debugging
            st.download_button(
                label="Download CV",
                data=html_content,
                file_name="naviai-cv.html",
                mime="text/html"
            )
            st.sidebar.text(f"Number of CVs generated: {get_cv_count()}")
        else:
            st.error("Failed to get edited CV from the API.")
            print("API Response:\n", cv_data)  # Print API response for debugging
    else:
        st.warning("Please provide both JD and CV.")
