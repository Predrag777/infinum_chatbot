# Koristi Python 3.9 kao osnovni image
FROM python:3.9

# Postavi radni direktorijum u kontejneru
WORKDIR /app

# Kopiraj fajlove u kontejner
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiraj ostatak koda u kontejner
COPY . .

# Pokreni Streamlit aplikaciju
CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
