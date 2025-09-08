# Usando a imagem oficial do python, com a tag alpine que é a mais enxuta
FROM python:alpine

# Determinando o diretório que será utilizado dentro do container
WORKDIR /app

# Copia o arquivo com as dependências
COPY requirements.txt .

# Instala as dependências presentes no aruivo de requirements
# a tag --no-cache-dir para evitar caches desnecessários
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto para o container
COPY . .

# Expõe a porta 5000, que é a pafrão para app Flask
EXPOSE 5000

ENV FLASK_APP=run.py

# Comando para rodar a aplicação quando o container iniciar
# O '--host=0.0.0.0' faz com que a aplicação seja acessível de fora do container
CMD ["flask", "run", "--host=0.0.0.0"]