# Package Sorting API

A REST API for sorting packages into appropriate stacks based on their dimensions and mass, designed for integration with robotic automation systems.

## Features

- **FastAPI-based REST API** with automatic OpenAPI documentation
- **Package sorting logic** based on volume and mass criteria
- **Input validation** with detailed error responses
- **Health check endpoint** for monitoring
- **Comprehensive test suite** with unit and integration tests
- **Async support** for high-performance concurrent requests

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Server

```bash
python src/main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

### Sorting Rules

- **STANDARD**: Packages that are neither bulky nor heavy
- **SPECIAL**: Packages that are bulky or heavy (but not both)
- **REJECTED**: Packages that are both bulky and heavy

Where:
- **Bulky**: Volume ≥ 1,000,000 cm³ OR any dimension ≥ 150 cm
- **Heavy**: Mass ≥ 20 kg

### Example Request

```bash
curl -X POST "http://localhost:8000/sort" \
     -H "Content-Type: application/json" \
     -d '{"width": 10.0, "height": 10.0, "length": 10.0, "mass": 5.0}'
```

Response:
```json
{"stack": "STANDARD"}
```

## Development

### Running Tests

```bash
# Unit tests
python -m pytest tests/unit/ -v

# Integration tests
python -m pytest tests/integration/ -v

# All tests
python -m pytest tests/ -v
```

### Project Structure

```
src/
├── api.py              # FastAPI application
├── main.py             # Server entry point
├── models.py           # Pydantic data models
└── sort_packages.py    # Core sorting logic

tests/
├── unit/               # Unit tests
└── integration/        # API integration tests

specs/                  # Feature specifications and plans
├── 001-number/
    ├── spec.md
    ├── plan.md
    ├── research.md
    ├── data-model.md
    ├── contracts/
    ├── quickstart.md
    └── tasks.md
```

## API Endpoints

### POST /sort
Sort a package into the appropriate stack.

**Request Body:**
```json
{
  "width": 10.0,
  "height": 10.0,
  "length": 10.0,
  "mass": 5.0
}
```

**Response:**
```json
{"stack": "STANDARD"}
```

### GET /health
Health check endpoint.

**Response:**
```json
{"status": "healthy"}
```

## Contributing

This project follows the Smarter Technologies constitution and development practices. See the `specs/` directory for detailed specifications and implementation plans.

## License

[Add license information]

## Decision Note

With 30 minutes I had a decision to make: build a basic function to sort using the "AND" and "OR" options, or run spec-kit and implement a secure API with observability and deploy as a Docker container. I chose the latter—implementing a secure (test-token based) API, observability (Prometheus + OpenTelemetry), and Docker-based reproducible environment while keeping the core sorting function minimal and well-tested.

If you want to test the function, follow the unit tests (`tests/unit/test_sort_packages.py`) or run the quick check script:

```bash
python scripts/run_unit_check.py
```

If you want to test the API, it requires integration with your OAuth infrastructure for production; currently the repo includes a minimal test-token/RBAC shim (`API_TEST_TOKEN` and `X-Roles` header) for local/dev verification. I can help integrate real OAuth2/JWT if you provide details about your identity provider.

As an expert developer I decided to use Python as the simplest language for this implementation. With the specification and tests in place, swapping the backend language or framework is straightforward — the spec, Pydantic models, and OpenAPI contract act as the source of truth for any reimplementation.

As this is a Senior Software Engineer role, I also opted to overdeliver and followed the spec-kit route: the repository now includes the generated `specs/001-number/` artifacts (plan, research, tasks, and contract stubs), a CI workflow, testing stubs, observability wiring, and a Docker-based reproducible environment. This makes it easier to iterate, verify requirements, and evolve the implementation or port it to another language when desired.