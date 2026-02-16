FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install sqlite3 only
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialize database
RUN python db_init.py

EXPOSE 8501

# Use a proper process manager or create a startup script
CMD ["sh", "-c", "python worker.py & streamlit run interface.py --server.port=8501 --server.address=0.0.0.0"]