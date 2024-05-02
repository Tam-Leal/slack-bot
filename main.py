import streamlit as st
import csv
from io import StringIO
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import random

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


def add_fontawesome():
    """
    Embeds FontAwesome CSS and a title with an icon into a Streamlit app.
    """
    # Inclui o CSS da FontAwesome
    fontawesome_css = ("<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css"
                       "/all.min.css'>")
    st.markdown(fontawesome_css, unsafe_allow_html=True)

    # HTML para o ícone de upload ao lado do texto "Upload CSV to Slack"
    icon_and_title_html = ('<span style="font-size: 1.7em; display: flex; align-items: center;"><i class="fas fa-paper-plane"'
                           ' style="font-size: 130%; padding-right: 0.5em;"></i> Slack Report Sync</span>')
    st.markdown(icon_and_title_html, unsafe_allow_html=True)


def generate_csv_data():
    """
    Simula dados CSV com 20 registros aleatórios e inclui uma nova coluna 'Department'.
    """
    # Cabeçalhos para os dados CSV
    headers = ["Name", "Age", "Email", "Department"]

    # Lista de nomes, departamentos e domínios de exemplo
    names = ["Greg", "Bob", "Charlie", "Alice", "Mary", "John", "Olivia", "James", "Linda", "Patricia",
             "Michael", "Laura", "Tom", "Diana", "Ethan", "Anna", "Peter", "Lucy", "Sam", "Nora"]
    departments = ["HR", "Marketing", "Sales", "Tech", "Support", "Finance", "Management", "Product", "Design",
                   "Operations"]

    # Gerando dados aleatórios
    data = [headers]  # Inicializa com cabeçalhos
    for i in range(20):  # Gerar 20 registros
        name = random.choice(names)
        age = random.randint(20, 60)
        email = f"{name.lower()}@example.com"
        department = random.choice(departments)
        data.append([name, age, email, department])

    # Cria um objeto StringIO para manter os dados CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerows(data)
    output.seek(0)  # Voltar ao início do stream para leitura
    return output.getvalue()


add_fontawesome()

# Gera e exibe os dados CSV como DataFrame assim que o app inicia
csv_data = generate_csv_data()
df = pd.read_csv(StringIO(csv_data))
st.dataframe(df)  # Mostra os dados na interface

# Usa as variáveis de ambiente para os inputs
token = os.getenv('SLACK_TOKEN')
channels = os.getenv('CHANNEL_ID')


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


# Usando colunas para centralizar o botão
col1, col2= st.columns([1,1])
with col1:
    if st.button('Upload Reports to Slack'):
        result = upload_file_to_slack(token, channels, csv_data, "data.csv")
        if result.get('ok'):
                st.success('File uploaded successfully to Slack!',icon="✅")
        else:
            st.error(f"Failed to upload file: {result.get('error')}")
