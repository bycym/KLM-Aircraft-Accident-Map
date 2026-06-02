FROM python:3.13-slim

WORKDIR /app
RUN pip install poetry==1.8.5
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --only main --no-root
COPY src ./src
ENV PYTHONPATH=/app/src
CMD ["python", "-m", "safety_database.main"]
