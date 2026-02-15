# Quickstart: Package Sorting API

## Overview

The package sorting API provides HTTP endpoints for sorting packages into STANDARD, SPECIAL, or REJECTED stacks based on their dimensions and mass.

## Installation

1. Ensure Python 3.11+ is installed
2. Install dependencies: `pip install fastapi uvicorn`
3. Clone or download the repository

## Running the API

Start the server:

```bash
python src/main.py
# or
uvicorn src.api:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Usage

### HTTP POST to /sort

```bash
curl -X POST "http://localhost:8000/sort" \
     -H "Content-Type: application/json" \
     -d '{"width": 10.0, "height": 10.0, "length": 10.0, "mass": 5.0}'
```

Response:
```json
{"stack": "STANDARD"}
```

### Python Client

```python
import requests

response = requests.post("http://localhost:8000/sort", json={
    "width": 10.0,
    "height": 10.0,
    "length": 10.0,
    "mass": 5.0
})
result = response.json()
print(result["stack"])  # "STANDARD"
```

### Direct Function Call

The core sorting logic is also available as a standalone function:

```python
from src.sort_packages import sort

stack = sort(width=10, height=10, length=10, mass=5)
print(stack)  # "STANDARD"
```

## Examples

### Standard Package
```json
POST /sort
{
  "width": 10.0,
  "height": 10.0,
  "length": 10.0,
  "mass": 5.0
}
```
Response: `{"stack": "STANDARD"}`

### Special Package (Bulky)
```json
POST /sort
{
  "width": 150.0,
  "height": 10.0,
  "length": 10.0,
  "mass": 5.0
}
```
Response: `{"stack": "SPECIAL"}`

### Special Package (Heavy)
```json
POST /sort
{
  "width": 10.0,
  "height": 10.0,
  "length": 10.0,
  "mass": 20.0
}
```
Response: `{"stack": "SPECIAL"}`

### Rejected Package
```json
POST /sort
{
  "width": 150.0,
  "height": 10.0,
  "length": 10.0,
  "mass": 20.0
}
```
Response: `{"stack": "REJECTED"}`

## Rules

- **Bulky**: Volume (width × height × length) ≥ 1,000,000 cm³ OR any dimension ≥ 150 cm
- **Heavy**: Mass ≥ 20 kg
- **STANDARD**: Neither bulky nor heavy
- **SPECIAL**: Bulky or heavy (but not both)
- **REJECTED**: Both bulky and heavy

## Health Check

```bash
curl http://localhost:8000/health
```

Response: `{"status": "healthy"}`

## Testing

Run unit tests:

```bash
python -m pytest tests/unit/
```

Run integration tests:

```bash
python -m pytest tests/integration/
```

## Integration

The API is designed for integration with robotic automation systems, conveyor belt controllers, and warehouse management software. It supports high concurrency and provides machine-readable JSON responses.