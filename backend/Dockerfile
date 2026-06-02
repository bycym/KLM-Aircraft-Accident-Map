FROM python:3.13-slim

WORKDIR /app
RUN pip install poetry==1.8.5
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --only main --no-root
COPY src ./src
ENV PYTHONPATH=/app/src
CMD ["uvicorn", "safety_backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
