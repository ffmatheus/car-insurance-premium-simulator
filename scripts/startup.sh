#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
/wait-for-postgres.sh db

echo "Applying database migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
uvicorn src.presentation.main:app --host 0.0.0.0 --port 8000 --reload