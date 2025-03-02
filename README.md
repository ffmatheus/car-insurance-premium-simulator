# Car Insurance Premium Simulator

A FastAPI service that calculates car insurance premiums based on a car's age, value, deductible percentage, and broker's fee. The application supports API key authentication and stores calculation history in a PostgreSQL database.

## Project Overview

This API simulates the calculation of car insurance premiums using a configurable rate system. The calculation considers:

- The age of the car (adding 0.5% per year to the rate)
- The value of the car (adding 0.5% per $10,000 of value)
- Optional geographic risk adjustment via GIS (Geographic Information System)

The application follows Domain-Driven Design (DDD), SOLID principles, and Clean Architecture to ensure maintainability and flexibility.

## Architecture

The project is structured following Clean Architecture principles:

- **Domain Layer**: Contains business rules, entities, value objects, and domain services
- **Application Layer**: Orchestrates use cases by coordinating domain objects
- **Infrastructure Layer**: Provides implementations for external services and database access
- **Presentation Layer**: Handles HTTP requests and responses via FastAPI endpoints

## Features

- Dynamic rate calculation based on car age and value
- Configurable parameters via environment variables
- API key authentication for secure access
- PostgreSQL database integration for storing calculation history
- GIS (Geographic Information System) adjustment based on location
- Docker containerization for easy deployment

## Requirements

- Python 3.10+
- FastAPI
- PostgreSQL
- Docker (recommended)

## Configuration

All calculation parameters are configurable via environment variables or a `.env` file:

```
# Calculation configuration
AGE_RATE_PER_YEAR=0.005      # Rate increase per year of car age (0.5%)
VALUE_RATE_PER_10000=0.005   # Rate increase per $10,000 of car value (0.5%)
VALUE_BRACKET=10000.0        # Value bracket size in dollars
DEFAULT_COVERAGE_PERCENTAGE=1.0  # Default coverage (100%)

# GIS configuration (optional)
ENABLE_GIS_ADJUSTMENT=true   # Enable/disable GIS-based rate adjustment
MAX_GIS_ADJUSTMENT=0.02      # Maximum positive GIS adjustment (+2%)
MIN_GIS_ADJUSTMENT=-0.02     # Maximum negative GIS adjustment (-2%)

# Authentication
API_KEY=api-key

# Database configuration
DATABASE_URL=postgresql://postgres:postgres@db:5432/car_insurance
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=car_insurance
```

## Installation and Setup

### Using Docker (recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build
```

This will start both the API service and PostgreSQL database.

### Database Migrations

The application uses Alembic for database migrations. If running outside Docker, you'll need to run migrations:

```bash
# Apply migrations
alembic upgrade head

# Create a new migration (when model changes are made)
alembic revision --autogenerate -m "description of changes"
```

### Using Poetry

```bash
# Install dependencies
poetry install

# Apply database migrations
poetry run alembic upgrade head

# Run the application
poetry run python -m src.presentation.main
```

### Using pip

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
alembic upgrade head

# Run the application
python -m src.presentation.main
```

## API Endpoints

All endpoints are protected with API key authentication. You need to include the `X-API-Key` header with your API key in all requests.

### Calculate Premium

**Endpoint**: `POST /premium/calculate`

**Headers**:
```
X-API-Key: api-key
```

**Request Body**:

```json
{
  "car": {
    "make": "Toyota",
    "model": "Corolla",
    "year": 2012,
    "value": 100000.0,
    "registration_location": {
      "city": "São Paulo",
      "state": "SP",
      "postal_code": "01310-200"
    }
  },
  "deductible_percentage": 0.10,
  "broker_fee": 50.0
}
```

**Response Body**:

```json
{
  "car": {
    "make": "Toyota",
    "model": "Corolla",
    "year": 2012,
    "value": 100000.0,
    "registration_location": {
      "city": "São Paulo",
      "state": "SP",
      "postal_code": "01310-200"
    }
  },
  "applied_rate": 0.10,
  "policy_limit": 90000.0,
  "calculated_premium": 9050.0,
  "deductible_value": 10000.0
}
```

### Get Premium History

**Endpoint**: `GET /premium/history`

**Headers**:
```
X-API-Key: your-secret-api-key-here
```

**Query Parameters**:
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)
- `car_make` (optional): Filter by car make
- `car_model` (optional): Filter by car model

**Response Body**:

```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "created_at": "2023-09-01T12:00:00.000000",
    "car": {
      "make": "Toyota",
      "model": "Corolla",
      "year": 2012,
      "value": 100000.0
    },
    "deductible_percentage": 0.10,
    "broker_fee": 50.0,
    "applied_rate": 0.10,
    "policy_limit": 90000.0,
    "calculated_premium": 9050.0
  },
  // ... more records
]
```

### Get Premium Calculation Details

**Endpoint**: `GET /premium/history/{calculation_id}`

**Headers**:
```
X-API-Key: your-secret-api-key-here
```

**Response Body**:

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "created_at": "2023-09-01T12:00:00.000000",
  "car": {
    "make": "Toyota",
    "model": "Corolla",
    "year": 2012,
    "value": 100000.0,
    "location": {
      "city": "São Paulo",
      "state": "SP",
      "postal_code": "01310-200"
    }
  },
  "calculation_parameters": {
    "deductible_percentage": 0.10,
    "broker_fee": 50.0
  },
  "calculation_results": {
    "applied_rate": 0.10,
    "base_premium": 10000.0,
    "deductible_value": 10000.0,
    "policy_limit": 90000.0,
    "calculated_premium": 9050.0
  },
  "request_data": { /* Original request JSON */ },
  "response_data": { /* Original response JSON */ }
}
```

## Running Tests

```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit

# Run only integration tests
pytest tests/integration

# Run with coverage report
pytest --cov=src
```

## Development

### Install Development Dependencies

```bash
poetry install --with dev
```

### Code Formatting and Linting

```bash
# Format code with Black
black src tests

# Sort imports with isort
isort src tests

# Check typing with mypy
mypy src

# Lint with flake8
flake8 src tests
```