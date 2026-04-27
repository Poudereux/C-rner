FROM python:3.11-slim

WORKDIR /streamlit

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

ENV API_URL=http://fastapi:8000

CMD ["streamlit", "run", "Library_A