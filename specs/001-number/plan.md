
# Implementation Plan: Package Sorting API

**Branch**: `001-number` | **Date**: 2026-02-15 | **Spec**: specs/001-number/spec.md
**Input**: Feature specification from `specs/001-number/spec.md`

**Note**: This plan was updated to reflect the amended specification (volume and dimension thresholds, mass rules, and the required `/sort` HTTP POST endpoint).

## Summary

Implement a deterministic, constant-time `sort(width, height, length, mass)` function that returns one of the stacks: `STANDARD`, `SPECIAL`, or `REJECTED` according to the amended rules in the spec. Expose the logic via an HTTP POST endpoint `POST /sort` that accepts JSON (`width`, `height`, `length`, `mass`) and returns `{ "stack": "..." }`.

Technical approach:
- Core business logic implemented in `src/sort_packages.py` as a pure function (O(1)).
- Pydantic models in `src/models.py` for request/response validation.
- API surface implemented with FastAPI (`src/api.py`) and run by `uvicorn` (`src/main.py`).
- Tests: unit tests for `sort()` in `tests/unit/`, integration tests for the endpoint in `tests/integration/`.

## Technical Context

**Language/Version**: Python 3.11 (project uses FastAPI and modern typing)  
**Primary Dependencies**: FastAPI, Pydantic, uvicorn, pytest  
**Storage**: N/A (stateless service)  
**Testing**: pytest (unit + integration)  
**Target Platform**: Containerized Linux/Windows server (runs under `uvicorn`)  
**Project Type**: Single backend service (API)  
**Performance Goals**: 200 req/s baseline; 99th percentile response <100ms in typical environment  
**Constraints**: Inputs must be validated (positive numeric dimensions/mass). Business logic must treat exact equality to thresholds as inclusive per spec (>= rules).  
**Scale/Scope**: Small service supporting automated systems; no persistent storage required.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Automation-Oriented API Design: API endpoint `POST /sort` returns JSON and is designed for machine consumption; `Health` endpoint present.
- [x] Security by Design: Input validation via Pydantic is planned; for production add auth (OAuth2/JWT) and rate limiting—documented as post-MVP tasks in `tasks.md`.
- [x] Scalability and Performance: Stateless service with `uvicorn` supports horizontal scaling; business logic is O(1).
- [x] Maintainability and Reliability: Clear separation between `src/sort_packages.py` (business logic), `src/models.py` (contracts), and `src/api.py` (HTTP layer). Tests exist and will be extended.
- [x] Observability and Monitoring: Logging is configured in `src/api.py`; plan to add metrics/health checks and integrate with platform monitoring.

## Project Structure

Documentation for this feature (under `specs/001-number/`):

```text
specs/001-number/
├── spec.md            # Feature spec (source of truth)
├── plan.md            # This file (implementation plan)
├── research.md        # Phase 0 output
├── data-model.md      # Phase 1 output (if needed)
├── quickstart.md      # Phase 1 output
└── contracts/         # OpenAPI or contract artifacts
```

Source layout (repository root):

```text
src/
├── api.py             # FastAPI app
├── main.py            # uvicorn runner
├── models.py          # Pydantic request/response models
├── sort_packages.py   # Business logic (sort function)
```

Tests:

```text
tests/
├── unit/test_sort_packages.py
├── unit/test_models.py
└── integration/test_api.py
```

**Structure Decision**: Keep existing single-backend project layout and implement the feature within `src/` to minimize churn.

## Complexity Tracking

No constitution violations requiring justification were identified. Security hardening (auth, rate-limiting) will be tracked as separate tasks but are out of scope for the MVP implementation.

