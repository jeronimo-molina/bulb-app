# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação para o diretório de trabalho
COPY . .

# Exponha a porta em que a aplicação será executada
EXPOSE 5000

# Defina a variável de ambiente para desativar o buffer de saída
ENV PYTHONUNBUFFERED=1

# Comando para rodar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.py"]
