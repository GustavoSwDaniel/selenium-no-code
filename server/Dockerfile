FROM python:3.11-slim

WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt ./

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala as dependências necessárias para o Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    --no-install-recommends && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copia o código-fonte para o container
COPY . .

ENV DATABASE_URL=postgresql+asyncpg://postgres:t8ltavvRLd@selenium:5432/postgres

EXPOSE 8080

# Comando para rodar a aplicação
CMD ["python", "src/app.py"]
