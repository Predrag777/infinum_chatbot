# Koristi Python 3.9 kao osnovni image
FROM python:3.9

# Postavi radni direktorijum u kontejneru
WORKDIR /app

# Kopiraj fajlove u kontejner
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiraj ostatak koda u kontejner
COPY . .

# Pokreni aplikaciju
CMD ["uvicorn", "API:app", "--host", "0.0.0.0", "--port", "8000"]
