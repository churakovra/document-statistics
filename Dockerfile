FROM python:3.13-slim as backend

WORKDIR /app

COPY requirements-backend.txt .
RUN pip install --no-cache-dir -r requirements-backend.txt

COPY app/ ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM python:3.13-slim as frontend

WORKDIR /app

COPY requirements-frontend.txt .
RUN pip install --no-cache-dir -r requirements-frontend.txt

COPY app-frontend/ ./app-frontend

EXPOSE 8501

CMD ["streamlit", "run", "app-frontend/frontend.py", "--server.address", "0.0.0.0", "--server.port", "8501"]