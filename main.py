import streamlit as st
import csv
from io import StringIO
import pandas as pd
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
    output.seek(0)  # Voltar ao início do stream para leitura
    return output.getvalue()

# Streamlit UI
st.title('CSV to Slack Uploader')

# Gera e exibe os dados CSV como DataFrame assim que o app inicia
csv_data = generate_csv_data()
df = pd.read_csv(StringIO(csv_data))
st.dataframe(df)  # Mostra os dados na interface

token = st.sidebar.text_input("Slack Token", type="password")
channels = st.sidebar.text_input("Channel ID")

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

if st.button('Upload CSV to Slack'):
    # Upload para Slack
    result = upload_file_to_slack(token, channels, csv_data, "data.csv")

    if result.get('ok'):
        st.success('File uploaded successfully to Slack!')
    else:
        st.error(f"Failed to upload file: {result.get('error')}")
