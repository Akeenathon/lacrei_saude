FROM python:3.13-slim


RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*


RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only=main

COPY . .

RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 3 --threads 2 --timeout 120 --max-requests 1000 --max-requests-jitter 100 --preload"]