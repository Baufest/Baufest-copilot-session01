FROM python:3.12-slim

# Install Poetry
RUN pip install --no-cache-dir poetry==2.4.1

WORKDIR /app

# Copy dependency files first to leverage Docker layer caching
COPY pyproject.toml poetry.lock* ./

# Install runtime dependencies only (no dev extras, no venv inside container)
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Copy application source
COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
