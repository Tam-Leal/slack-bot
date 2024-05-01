# Usar uma imagem base oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo de requerimentos e instalar as dependências
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copiar os arquivos restantes do projeto para o container
COPY . .

# Expõe a porta 8501, usada pelo Streamlit
EXPOSE 8501

# Comando para rodar a aplicação
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
