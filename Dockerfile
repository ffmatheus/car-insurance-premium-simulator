FROM python:3.10-slim as base

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false

RUN poetry install --only main

COPY src/ ./src/
COPY migrations/ ./migrations/
COPY alembic.ini ./alembic.ini

COPY scripts/wait-for-postgres.sh /wait-for-postgres.sh
COPY scripts/startup.sh /startup.sh
RUN chmod +x /wait-for-postgres.sh /startup.sh

CMD ["/startup.sh"]