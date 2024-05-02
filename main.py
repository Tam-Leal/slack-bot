import streamlit as st
import csv
from io import StringIO
import requests


def generate_csv_data():
    # Simula dados CSV
    data = [["Name", "Age", "Email"],
            ["Greg", 28, "greg@example.com"],
            ["Bob", 24, "bob@example.com"],
            ["Charlie", 30, "charlie@example.com"]]

    # Cria um objeto StringIO para manter os dados CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerows(data)
    return output.getvalue()


def upload_file_to_slack(token, channels, file_content, filename):
    url = "https://slack.com/api/files.upload"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "channels": channels,
        "content": file_content,
        "filename": filename,
        "filetype": "auto",
        "initial_comment": "Sir, here is your file!"
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()


# Streamlit UI
st.title('CSV to Slack Uploader')

token = st.sidebar.text_input("Slack Token", type="password")
channels = st.sidebar.text_input("Channel ID")

if st.button('Generate and Upload CSV'):
    # Gera dados CSV
    csv_data = generate_csv_data()

    # Upload para Slack
    result = upload_file_to_slack(token, channels, csv_data, "data.csv")

    if result.get('ok'):
        st.success('File uploaded successfully to Slack!')
    else:
        st.error(f"Failed to upload file: {result.get('error')}")
