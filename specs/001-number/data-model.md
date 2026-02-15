# Data Model: Package Sorting API

## Entities

### Package
Represents a physical package with dimensions and mass for sorting operations.

**Fields**:
- `width` (float): Width in centimeters, must be > 0
- `height` (float): Height in centimeters, must be > 0
- `length` (float): Length in centimeters, must be > 0
- `mass` (float): Mass in kilograms, must be > 0

**Relationships**: None (standalone entity)

**Validation Rules**:
- All dimensions and mass must be positive numbers
- No upper bounds specified (implementation handles large values)

**State Transitions**: N/A (stateless sorting operation)

**Business Rules**:
- Bulky if volume ≥ 1,000,000 cm³ OR any dimension ≥ 150 cm
- Heavy if mass ≥ 20 kg
- Sorting priority: REJECTED (both bulky and heavy) > SPECIAL (bulky or heavy) > STANDARD (neither)

## API Models

### PackageRequest
Request model for API endpoint.

**Fields**:
- `width` (float): Package width in cm
- `height` (float): Package height in cm
- `length` (float): Package length in cm
- `mass` (float): Package mass in kg

**Validation**: All fields required, must be positive numbers

### PackageResponse
Response model for API endpoint.

**Fields**:
- `stack` (string): Sorting result ("STANDARD", "SPECIAL", or "REJECTED")

**Validation**: Must be one of the allowed enum values

### ErrorResponse
Error response model.

**Fields**:
- `error` (string): Error message description

**Validation**: Error message must be descriptive